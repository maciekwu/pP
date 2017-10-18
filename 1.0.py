import pymysql

class Projekt:

    def __init__(self, mail):
        self.conn = pymysql.connect('localhost', 'python_user', 'niebieski123', 'projektt', charset='utf8')
        #ustawienie kursora
        self.cursor = self.conn.cursor()
        self.mail = mail
        while(True):
            initial_choice = input('___________________\n-= Login page =-\n|  L - Log in |  R - Register |  Q - Quit  |\nYour choice: ').upper()
                
            if (initial_choice == 'L'):
                loginSuccessfull = self.login()
                while(loginSuccessfull):
                # TODO: what to do after successul login
                    choice = input('___________________\n-= Main menu =-\n|  A - Add a friend  |  F - List your friends  |  L - Location  |  Q - Quit  |\nYour choice: ').upper()
                    if (choice == 'A'):
                        self.addFriend(mail)
                    
                    if (choice == "F"):
                        self.printFriend(mail)
                        
                    if (choice == "L"):
                        self.location(mail)   
                        
                    if (choice == 'Q'):
                        print('___________________\nSuccessfull logout.')
                        break                    
            
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
        self.cursor.execute("SELECT * FROM LOGOWANIE WHERE MAIL = '%s' AND PASSWRD = '%s';" % (mail, passwrd_))
        RS = self.cursor.fetchall()
        # check if given mail and password are correct
        # if Y: log in
        if(len(RS) != 0):
            print('___________________\nSuccessfull login!')
            return True

        # if N: ask for mail and password again <- correct so that main menu is being displayed
        else:
            print('___________________\n!Wrong credentials. Please try again.')
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
                self.cursor.execute("INSERT INTO LOGOWANIE (MAIL, PASSWRD, ID_U) values ('%s', '%s', (select id from Uzytkownicy where mail = '%s'));" %(mail_, passwrd_, mail_))
                self.conn.commit()
                print('___________________\nGREAT! User %s added successfully.' %(mail_))
                break
        

        
    def addFriend(self, mail):
        self.mail = mail
        print('___________________\nADD A FRIEND\n___________________')
        fMail = input('Who would you like to tag as a friend: ')
        # check if future friend exists in db
        self.cursor.execute("SELECT * FROM UZYTKOWNICY WHERE UPPER(MAIL) = UPPER('%s');" %(fMail))
        RS = self.cursor.fetchall()            
        # if Y   
        if(len(RS) != 0):
            # check if he is already a friend
            self.cursor.execute("select mail from uzytkownicy where id in (select id_z from relacje where id_u = (select id from uzytkownicy where mail = '%s'));" %(mail))
            RS_ = self.cursor.fetchall()
            # if N: add user to friends list
            if (len(RS_) == 0):
                # two records to be created in RELACJE table: for relation current user - new friend and new friend - current user
                self.cursor.execute("INSERT INTO Relacje (TYP_RELACJI, ID_U, ID_Z) values ('%s', (select id from Uzytkownicy where mail = '%s'), (select id from Uzytkownicy where mail = '%s'));" %('F', mail, fMail))
                self.cursor.execute("INSERT INTO Relacje (TYP_RELACJI, ID_U, ID_Z) values ('%s', (select id from Uzytkownicy where mail = '%s'), (select id from Uzytkownicy where mail = '%s'));" %('F', fMail, mail))
                self.conn.commit()            
                print('___________________\nUser %s has been successfully added to your friends list!' % (fMail))
            else:
                print('___________________\nYou are already friends with user %s.' %(fMail))
        else:            
                print('___________________\nUser %s does not exist!' %(fMail))
            
    def findFriend(self):
        print('Znalazles')
    
    def printFriend(self, mail):
        print('___________________\nYOUR FRIENDS LIST\n___________________')
        self.mail = mail
        self.cursor.execute("select mail from uzytkownicy where id in (select id_z from relacje where id_u = (select id from uzytkownicy where mail = '%s'));" %(mail))
        RS = self.cursor.fetchall()
        for friend in RS:
            print('*', friend[0])
    
    def location(self, mail):
        print('___________________\nCHECK IN TO YOUR LOCATION\n___________________')
        self.mail = mail
        self.cursor.execute("SELECT nazwa FROM miejsca WHERE id = (SELECT id_m FROM lokacja WHERE id_u = (SELECT id FROM uzytkownicy WHERE mail = '%s'));" %(mail))
        alreadyCheckInTo = self.cursor.fetchall()
        # check if user is already check in to some place
        if (len(alreadyCheckInTo) != 0):
            # if Y: print where is user checked in
            while(True):
                # if Y: print where is user checked in
                print('You are already checked in to: %s' % (alreadyCheckInTo[0]))
                # ask for check out from current place
                checkOutDec = input('Would you like to check out from %s? [Y / N]: ' % (alreadyCheckInTo[0])).upper()
                # if N: go back to main menu
                if (checkOutDec == 'N'):
                    break
                # if N: delete record from LOKACJA table and proceed further
                else:
                    self.cursor.execute("DELETE FROM lokacja WHERE id_u = (SELECT id FROM uzytkownicy WHERE mail = '%s');" %(mail))
                    self.conn.commit()                    
                    print('You have been successfully checked out from %s.' % (alreadyCheckInTo[0]))
                    return False
        else:
            # if N: list available places to check in
            print('Available places:\n___________________')
            self.cursor.execute("SELECT nazwa FROM miejsca")
            PLACES = self.cursor.fetchall()
            for place in PLACES:
                print('* ', place[0]) 
            # ask where to check in
            while (True):
                checkTo = input('Where would you like to check in [type name]: ').upper()
                # check if user provided correct place name
                self.cursor.execute("SELECT nazwa FROM miejsca WHERE UPPER(nazwa) = UPPER('%s');" % (checkTo))
                placeExist = self.cursor.fetchall()
                # if Y: check in user to selected place
                if(len(placeExist) != 0):
                    self.cursor.execute("INSERT INTO lokacja (id_u, id_m) VALUES((SELECT id FROM uzytkownicy WHERE mail = '%s'), (SELECT id FROM miejsca WHERE UPPER(nazwa) = UPPER('%s')));" %(mail, checkTo))
                    self.conn.commit()
                    print('You have been successfully checked in to %s.' %(checkTo))
                    break
                # if N: ask to provide place's name again until correct
                else:
                    print('Please provide correct place name.')
                    
                
        
    def locationCheckOut(self, mail):
        print('___________________\nCHECK OUT FROM YOUR LOCATION\n___________________')
        self.mail = mail
        

        
    
    def logout(self):
        print('Zostales pomyslnie wylogowany')
        
    def deleteAccount():
        print('Konto usuniete pomyslnie')
        
    # TODO: po co jest:     def DBclose(self): /         print('Koniec') /         self.conn.close()
    # TODO: klasy testowe i ROZDZIELENIE NA KLASY !!!!!
    # haslo do bazy w osobnej bibliotece
    # TODO: uniemozliwienie podgladania lokalizacji nie-przyjaciela

sql = Projekt('mck')