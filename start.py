import pymysql
import passPackage.keepPass
import LoginPage
import mail
import sqlConnection
        

class start:

    def __init__(self):
        sqlConnection.sqlConnectionClass.__init__(self)
        while(True):
            # display Login page
            LoginPage.LoginPage.__init__()
            # ask user what to do
            initial_choice = input('Make a choice: ').upper()
            if (initial_choice == 'L'):
                isLoggedIn = self.login()
                while(isLoggedIn):
                    # display user's Main menu after successfull login
                    print(' _____________________________________________________________')
                    print('|                     -= Main menu =-                         |')
                    print('|                                                             |')
                    print('|                   A - Add a friend                          |')
                    print('|       L - Your Location  |  F - Find your friend(s)         |')
                    print('|                      M - Messages                           |')
                    print('|                   R - Rate your visit                       |')
                    print('|                      Q - Log out                            |')
                    print('|_____________________________________________________________|')                       

                    # ask logged user what to do
                    choice = input('Your choice: ').upper()
                    if (choice == 'A'):
                        self.addFriend(self.mail)
                        continue
                    
                    elif (choice == "F"):
                        self.checkFriendLocationAndRating(self.mail)
                        continue
                        
                    elif (choice == "L"):
                        self.setYourLocation(self.mail) 
                        continue
                        
                    elif (choice == 'M'):
                        mail.mail(self.mail)
                        continue
                    
                    elif (choice == 'R'):
                        self.rateYourVisit(self.mail)
                        continue                    
                        
                    elif (choice == 'Q'):
                        print('___________________\nSuccessfull logout.')
                        break 
                    
                    else:
                        print('Pardonn?')                        
            
            if (initial_choice == 'R'):
                self.register()
            
            elif (initial_choice == 'Q'):
                print('___________________\nBye, bye!')
                break    
            
            else:
                print('Pardon?')                             
                
    def login(self):
        print('.___________________.')
        print('|      LOG IN       |')
        print('|___________________|')        
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
        self.mail = mail     
        while(True):            
            print('.___________________________.')
            print('|  YOUR FRIENDS\' LOCATION  |')
            print('|___________________________|')
            print('1 - Friends in same location')
            print('2 - All checked-in Friends')
            print('3 - Not checked-in Friends')
            print('4 - Back to main menu')
            whatToDo = input('Select an option: ')
            # ask db whether current user is already checked in to anywhere
            self.cursor.execute("SELECT who, where_is from userinlocationrating where who = '%s'" %(self.mail))
            alreadyCheckInTo = self.cursor.fetchall()               
            if (int(whatToDo) == 1):
                # check if user is already checked in to anywhere
                if(len(alreadyCheckInTo) != 0):
                    # if Y: ask db for location of friends in same location
                    self.cursor.execute("select who, where_is, rating from userinlocationrating where isFriendOf = '%s' and where_is = '%s';" %(self.mail, alreadyCheckInTo[0][1]))
                    friendsCheckedInNearYou = self.cursor.fetchall()
                    # check if any checked in friends exist
                    if (len(friendsCheckedInNearYou) != 0):
                        # if Y: print friends and their locations
                        for who, whereIs, rating in friendsCheckedInNearYou:
                            print('User: %15s  |  Location: %15s  |  Rating: %15s  |'  %(who, whereIs, str(rating)))
                            continue
                    # if N: print message    
                    else:
                        print('Nobody has checked in at your place.')
                        continue
                else:
                    print('You are not checked in! Select location first.')
                    continue
                
            if (int(whatToDo) == 2):
                if(len(alreadyCheckInTo) != 0):
                    # ask db for location of friends who are check in anywhere
                    self.cursor.execute("select who, where_is, rating from userinlocationrating where isFriendOf = '%s'  and where_is != 'is Unchecked';" %(self.mail))
                    allCheckedInFriendsList = self.cursor.fetchall()
                    # check if any checked in friends exist
                    if (len(allCheckedInFriendsList) != 0):
                        # if Y: print friends and their locations
                        for who, whereIs, rating in allCheckedInFriendsList:
                            print('User: %15s  |  Location: %15s  |  Rating: %15s  |'  %(who, whereIs, str(rating)))
                        continue
                    # if N: print message    
                    else:
                        print('Nobody near you.')
                        continue
                else:
                    print('You are not checked in! Select location first.')
                    continue 
            
            if (int(whatToDo) == 3):
                if(len(alreadyCheckInTo) != 0):
                    # ask db for location of friends who are not checked in
                    self.cursor.execute("select who from userinlocationrating where isFriendOf = '%s' and where_is = 'is Unchecked';" %(self.mail))
                    allNotCheckedInFriendsList = self.cursor.fetchall()
                    # check if any not checked in friends exist
                    if (len(allNotCheckedInFriendsList) != 0):
                        # if Y: print friends and their locations
                        for who in allNotCheckedInFriendsList:
                            print('Users that have not checked in: ')
                            print('* %s'  %(who))
                            continue
                    # if N: print message    
                    else:
                        print('Nobody near you.')
                        continue
                else:
                    print('You are not checked in! Select location first.')
                    continue
                    
            if (int(whatToDo) == 4):
                break
            else:
                print('Select once again.')
                break
                
            print('You don\'t have any friends :(')
    
    def setYourLocation(self, mail):          
        self.mail = mail
        while(True):
            print('.___________________________.')
            print('|     SET YOUR LOCATION     |')
            print('|___________________________|')              
            # ask db whether user is already checked in anywhere
            self.cursor.execute("SELECT nazwa FROM miejsca WHERE id = (SELECT id_place FROM lokacja WHERE id_user = (SELECT id FROM uzytkownicy WHERE mail = '%s'));" %(self.mail))
            alreadyCheckInTo = self.cursor.fetchall()
            # check if user is already check in to some place
            if (len(alreadyCheckInTo) != 0):
                # if Y: print where is user checked in
                print('You are already checked in to: %s' % (alreadyCheckInTo[0]))
                # ask if user would like to check out from current place
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
                    continue
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
                        
                                            
    def rateYourVisit(self, mail):
        print('___________________\nRATE YOUR VISIT\n___________________')
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
                        # delete previous rating
                        self.cursor.execute("Delete from Ocena where id_user = (select id from uzytkownicy where mail = '%s') and id_place = (select id from miejsca where nazwa = '%s');" %(who, whereIs))
                        self.conn.commit()
                        # add new rating
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
    # osobna klasa z komunikatami, np. "sele once again" / "wrong choice"

obiektKlasyMain = start()