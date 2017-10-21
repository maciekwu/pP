import pymysql

class Projekt:

    def __init__(self):
        self.conn = pymysql.connect('localhost', 'python_user', 'niebieski123', 'projektt', charset='utf8')
        #ustawienie kursora
        self.cursor = self.conn.cursor()
        while(True):
            # display Login page
            print('___________________\n-= Login page =-\n|  L - Log in |  R - Register |  Q - Quit  |')
            # ask user what to do
            initial_choice = input('Your choice: ').upper()
            if (initial_choice == 'L'):
                isLoggedIn = self.login()
                while(isLoggedIn):
                    # display user's Main menu after successfull login
                    print('___________________\n-= Main menu =-\n|  A - Add a friend  |  F - Find your friend(s)  |  L - Location  |  \n|  S - send a massage  |  M - Messages  |  R - Rate your visit  |  Q - Log out %s |' %(self.mail))
                    # ask logged user what to do
                    choice = input('Your choice: ').upper()
                    if (choice == 'A'):
                        self.addFriend(self.mail)
                        continue
                    
                    if (choice == "F"):
                        self.checkFriendLocationAndRating(self.mail)
                        continue
                        
                    if (choice == "L"):
                        self.setYourLocation(self.mail) 
                        continue
                        
                    if (choice == 'S'):
                        self.sendMessage(self.mail)
                        continue
                        
                    if (choice == 'M'):
                        self.readMessage(self.mail)
                        continue
                    
                    if (choice == 'R'):
                        self.rateYourVisit(self.mail)
                        continue                    
                        
                    if (choice == 'Q'):
                        print('___________________\nSuccessfull logout.')
                        break 
                    
                    else:
                        print('Pardonn?')                        
            
            if (initial_choice == 'R'):
                self.register()
            
            if (initial_choice == 'Q'):
                print('___________________\nBye, bye!')
                break    
            
            if (initial_choice != 'L' and initial_choice != 'R' and initial_choice != 'Q' ):
                print('Pardon?')                             
                
    def login(self):
        print('___________________\nLOG IN\n___________________')        
        mail = input('Your Mail: ')
        self.mail = mail
        passwrd_ = input('Password: ') 
        self.cursor.execute("SELECT * FROM LOGOWANIE WHERE MAIL = '%s' AND PASSWRD = '%s';" % (self.mail, passwrd_))
        RS = self.cursor.fetchall()
        # check if given mail and password are correct
        # if Y: log in
        if(len(RS) != 0):
            print('___________________\nSuccessfull login!')
            return True

        # if N: go back to Login page
        else:
            print('___________________\nWrong credentials. Please try again.')
            return False
        
    def register(self):
        print('___________________\nREGISTER\n___________________')
        # check if given mail already exists in db
        while(True):
            mail_ = input('Your mail: ')
            self.cursor.execute("SELECT * FROM UZYTKOWNICY WHERE UPPER(MAIL) = UPPER('%s');" %(mail_))
            RS = self.cursor.fetchall()
            # if Y: back to home page
            if(len(RS) != 0):
                print('___________________\nUser already exists! Try another one.')
                break
            # if N: ask for remaining credentials
            else:              
                imie_ = input('Name: ')
                miasto_ = input('City: ')
                passwrd_ = input('Password: ')
                # pass credentials to db  
                # insert record to table: UZYTKOWNICY 
                self.cursor.execute("INSERT INTO Uzytkownicy (IMIE, MIASTO, MAIL) values ('%s', '%s', '%s');" %(imie_, miasto_, mail_))
                self.conn.commit()
                
                # insert record to table: LOGOWANIE 
                self.cursor.execute("INSERT INTO LOGOWANIE (MAIL, PASSWRD, id_user) values ('%s', '%s', (select id from Uzytkownicy where mail = '%s'));" %(mail_, passwrd_, mail_))
                self.conn.commit()
                print('___________________\nGREAT! User %s added successfully.' %(mail_))
                break
        
        
    def addFriend(self, mail):
        self.mail = mail
        print('___________________\nADD A FRIEND\n___________________')
        friendMail = input('Who would you like to tag as a friend: ')
        # check if future friend exists in db
        self.cursor.execute("SELECT * FROM UZYTKOWNICY WHERE UPPER(MAIL) = UPPER('%s');" %(friendMail))
        RS = self.cursor.fetchall()            
        # if Y   
        if(len(RS) != 0):
            # check if he is already a friend
            self.cursor.execute("select * from relacje where id_user = (select id from uzytkownicy where mail = '%s') and id_friend = (select id from uzytkownicy where mail = '%s');" %(self.mail, friendMail))
            RS_ = self.cursor.fetchall()
            # if N: add user to friends list
            if (len(RS_) == 0):
                # two records to be created in RELACJE table: for relation current user - new friend and new friend - current user
                self.cursor.execute("INSERT INTO Relacje (TYP_RELACJI, id_user, id_friend) values ('%s', (select id from Uzytkownicy where mail = '%s'), (select id from Uzytkownicy where mail = '%s'));" %('F', self.mail, friendMail))
                self.cursor.execute("INSERT INTO Relacje (TYP_RELACJI, id_user, id_friend) values ('%s', (select id from Uzytkownicy where mail = '%s'), (select id from Uzytkownicy where mail = '%s'));" %('F', friendMail, self.mail))
                self.conn.commit()            
                print('___________________\nUser %s has been successfully added to your friends list!' % (friendMail))
            else:
                print('___________________\nYou are already friends with user %s.' %(friendMail))
        else:            
                print('___________________\nUser %s does not exist!' %(friendMail))
            
    
    def checkFriendLocationAndRating(self, mail):
        print('___________________\nYOUR FRIENDS\' LOCATION\n___________________')
        self.mail = mail
        # set cursor
        self.cursor.execute("select mail from uzytkownicy where id in (select id_friend from relacje where id_user = (select id from uzytkownicy where mail = '%s'));" %(self.mail))
        # fetch cursor with list of friends
        friendsList = self.cursor.fetchall()
        # check if any friends exist
        # if Y: print friends and their locations
        if (len(friendsList) != 0):            
            # set cursor
            self.cursor.execute("select who, isFriendOf, where_is, rating from userinlocationrating where isFriendOf = '%s';" %(self.mail))
            # fetch cursor with list of friends,their locations and their rating of visit
            friendsInLocationsList = self.cursor.fetchall()
            for who, isFriendOf, whereIs, rating in friendsInLocationsList:
                print('User: %15s  |  Location: %15s  |  Rating: %10s  |'  %(who, whereIs, str(rating)))
        # if N: print message    
        else:
            print('You don\'t have any friends :(')
    
    def setYourLocation(self, mail):
        print('___________________\nCHECK IN TO YOUR LOCATION\n___________________')
        self.mail = mail
        self.cursor.execute("SELECT nazwa FROM miejsca WHERE id = (SELECT id_place FROM lokacja WHERE id_user = (SELECT id FROM uzytkownicy WHERE mail = '%s'));" %(self.mail))
        alreadyCheckInTo = self.cursor.fetchall()
        # check if user is already check in to some place
        if (len(alreadyCheckInTo) != 0):
            # if Y: print where is user checked in
            while(True):
                # if Y: print where is user checked in
                print('___________________\nYou are already checked in to: %s' % (alreadyCheckInTo[0]))
                # ask for check out from current place
                checkOutDec = input('Would you like to check out from %s? [Y / N]: ' % (alreadyCheckInTo[0])).upper()
                # if N: go back to main menu
                if (checkOutDec == 'N'):
                    break
                # if N: delete record from LOKACJA table and proceed further
                else:
                    self.cursor.execute("DELETE FROM lokacja WHERE id_user = (SELECT id FROM uzytkownicy WHERE mail = '%s');" %(self.mail))
                    self.conn.commit()  
                    self.cursor.execute("DELETE FROM ocena WHERE id_user = (SELECT id FROM uzytkownicy WHERE mail = '%s');" %(self.mail))
                    self.conn.commit() 
                    print('___________________\nYou have been successfully checked out from %s.' % (alreadyCheckInTo[0]))
                    break
        else:
            # if N: list available places to check in
            print('Available places:\n___________________')
            self.cursor.execute("SELECT nazwa FROM miejsca where miasto = (select miasto from uzytkownicy where mail = '%s');" % (self.mail))
            PLACES = self.cursor.fetchall()
            for place in PLACES:
                print('* ', place[0]) 
            # ask where to check in
            while (True):
                checkTo = input('___________________\nWhere would you like to check in [type place\'s name]: ').upper()
                # check if user provided correct place name
                self.cursor.execute("SELECT nazwa FROM miejsca WHERE UPPER(nazwa) = UPPER('%s') and miasto = (select miasto from uzytkownicy where mail = '%s');" % (checkTo, self.mail))
                placeExist = self.cursor.fetchall()
                # if Y: check in user to selected place
                if(len(placeExist) != 0):
                    self.cursor.execute("INSERT INTO lokacja (id_user, id_place) VALUES((SELECT id FROM uzytkownicy WHERE mail = '%s'), (SELECT id FROM miejsca WHERE UPPER(nazwa) = UPPER('%s')));" %(self.mail, checkTo))
                    self.conn.commit()
                    print('You have been successfully checked in to %s.' %(checkTo))
                    break
                # if N: ask to provide place's name again until correct
                else:
                    print('Incorrect place\' name. Please provide correct name.')
                    
                
    def sendMessage(self, mail):
        self.mail = mail
        print('___________________\nSEND MESSAGE\n___________________')
        while(True):
            # ask for mail of a friend to whom you would like to send a message
            messRecipientMail = input('Send message to: ')
            self.cursor.execute("select id_user from relacje where id_friend = (select id from uzytkownicy where mail = '%s');" %(messRecipientMail))
            # fetch cursor
            isFriend = self.cursor.fetchall()
            # check if given mail belongs to any of your friends AND given mail is not your mail
            # if Y: ask for message content
            if (len(isFriend) != 0 ) and (messRecipientMail != self.mail):               
                messContent = input('Message (max 100 chars - TEST): ')                
                # add message, author and recipient to db
                self.cursor.execute("insert into wiadomosci (tresc, id_user, id_friend) values (SUBSTR('%s', 1, 100), (select id from Uzytkownicy where mail = '%s'), (select id from Uzytkownicy where mail = '%s'));" %(messContent, self.mail, messRecipientMail))
                self.conn.commit()
                print('Message has been sent.')
                break
            # if N:    
            else:
                print('You are not a friend of %s' %(messRecipientMail)) 
                break
            
    def readMessage(self, mail):
        self.mail = mail
        print('___________________\nREAD MESSAGE\n___________________')
        self.cursor.execute("select author, content from messageauthorread where is_read = '0' and recipient = '%s';" %(self.mail))
        # fetch cursor
        newMessages = self.cursor.fetchall()
        # check if there are any unreaded messages - IMPORTANT: only unreaded messages are being shown here
        # if Y: print them
        if (len(newMessages) != 0 ):
            # count number of new messages
            self.cursor.execute("select count(*) from messageauthorread where is_read = '0' and recipient = '%s';" %(self.mail))
            numOfNewMessages = self.cursor.fetchall()
            # display number of new messages
            print('You have %s new message(s):\n___________________.' %(numOfNewMessages[0]))
            for author, content in newMessages:
                print('* New message from %s: %s' %(author, content))
                # mark message as already readed
                self.cursor.execute("update wiadomosci set is_read = '1' where id_friend = (select id from uzytkownicy where mail = '%s');" %(self.mail))
                self.conn.commit()                                
        # if N:     
        else:
            print('You have no new messages') 
                                    
    def rateYourVisit(self, mail):
        print('___________________\nRATE YOUR VISIT\n___________________')
        self.mail = mail
        self.cursor.execute("SELECT who, where_is from userinlocationrating where who = '%s' and where_is != 'is Unchecked';" %(self.mail))
        alreadyCheckInTo = self.cursor.fetchall()
        # check if user is already check in to some place
        if (len(alreadyCheckInTo) != 0):
            while(True):
                # if Y: ask for rating
                rating = int(input('Rate your visit in %s [1 - 5]: ' %(alreadyCheckInTo[0][1])))
                # check if rating in [1 - 5]
                if (rating in range(6)):					
                    # insert rating to db
                    for who, whereIs in alreadyCheckInTo:
                        self.cursor.execute("INSERT into Ocena (ocena, id_user, id_place) values (%i, (select id from uzytkownicy where mail = '%s'), (select id from miejsca where nazwa = '%s'));" %(rating, who, whereIs))
                        self.conn.commit() 
                        print('You have successfully rated %s!' % (alreadyCheckInTo[0][1]))
                        break
                    break
                # if N: ask for rating again
                else:
                    print('Please provide rating from 1 to 5.')
                    continue
        else:
            print('Set your location first!')           
        
    def deleteAccount():
        print('Konto usuniete pomyslnie')
        
    # TODO: po co jest:     def DBclose(self): /         print('Koniec') /         self.conn.close()
    # TODO: klasy testowe i ROZDZIELENIE NA KLASY !!!!!
    # TODO: haslo do bazy w osobnej bibliotece
    # TODO: metoda deleteAccount() <--- usuwanie danych ze wszystkich tabel
    # TODO: metoda deleteFriend()
    # TODO: podmien selecty z tabel na selecty z widokow
    # TODO: sortowanie wyswietlania listy znajomych po lokacji, w ktorej jestes Ty


sql = Projekt()