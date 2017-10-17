import pymysql

class Projekt:

    def __init__(self, mail):
        self.conn = pymysql.connect('localhost', 'python_user', 'niebieski123', 'projektt', charset='utf8')
        #ustawienie kursora
        self.cursor = self.conn.cursor()
        self.mail = mail
        while(True):
            initial_choice = input('___________________\n|  L - Log in |  R - Register |  Q - Quit  |\nYour choice: ').upper()
                
            if (initial_choice == 'L'):
                self.login()
                # TODO: totaj kolejny wybor co chce robic
                choice = input('___________________\nWELCOME\n|  A - Add a friend|  Q - Quit  |\nYour choice: ').upper()
                if (choice == 'A'):
                    self.addFriend(mail)
                    
                if (choice == 'Q'):
                    print('Bye, bye!')
                    break                 
            
            if (initial_choice == 'R'):
                self.register()
            
            if (initial_choice == 'Q'):
                print('Bye, bye!')
                break    
            
            if (initial_choice != 'L' and initial_choice != 'R' and initial_choice != 'Q' ):
                print('Pardon?')              
                  
                
    def login(self):
        print('___________________\nLOG IN\n___________________')
        # check if given mail and password are correct
        while(True):
            mail = input('Mail: ')
            self.mail = mail
            passwrd_ = input('Password: ') 
            self.cursor.execute("SELECT * FROM LOGOWANIE WHERE MAIL = '%s' AND PASSWRD = '%s';" % (mail, passwrd_))
            RS = self.cursor.fetchall()
            # if Y: log in
            if(len(RS) != 0):
                print('___________________\nSuccessfull login!')
                break
            # if N: ask for mail and password again
            else:
                print('___________________\n!!! Wrong credentials. Please try again.')
                continue
        
    def register(self):
        print('___________________\nREGISTER\n___________________')
        # check if given mail already exists in db
        while(True):
            mail_ = input('Your mail: ')
            self.cursor.execute("SELECT * FROM UZYTKOWNICY WHERE UPPER(MAIL) = UPPER('%s');" %(mail_))
            RS = self.cursor.fetchall()
            # if Y: ask for mail again
            if(len(RS) != 0):
                print('___________________\nUser already exists! Try another e-mail.\n___________________')
                continue
            # if N: ask for remaining credentials
            else:              
                imie_ = input('Name: ')
                miasto_ = input('City: ')
                passwrd_ = input('Password: ')
                break
        # pass credentials to db  
        # insert record to table: UZYTKOWNICY 
        self.cursor.execute("INSERT INTO Uzytkownicy (IMIE, MIASTO, MAIL) values ('%s', '%s', '%s');" %(imie_, miasto_, mail_))
        self.conn.commit()
        
        # insert record to table: LOGOWANIE 
        self.cursor.execute("INSERT INTO LOGOWANIE (MAIL, PASSWRD, ID_U) values ('%s', '%s', (select id from Uzytkownicy where mail = '%s'));" %(mail_, passwrd_, mail_))
        self.conn.commit()
        
        print('___________________\nGREAT! User added successfully.')
        
    def addFriend(self, mail):
        self.mail = mail
        fMail = input('What is your friend\'s mail: ')
        self.cursor.execute("SELECT * FROM UZYTKOWNICY WHERE UPPER(MAIL) = UPPER('%s');" %(fMail))
        RS = self.cursor.fetchall()
        if(len(RS) != 0):
            self.cursor.execute("INSERT INTO Relacje (TYP_RELACJI, ID_U, ID_Z) values ('%s', (select id from Uzytkownicy where mail = '%s'), (select id from Uzytkownicy where mail = '%s'));" %('F', mail, fMail))
            self.cursor.execute("INSERT INTO Relacje (TYP_RELACJI, ID_U, ID_Z) values ('%s', (select id from Uzytkownicy where mail = '%s'), (select id from Uzytkownicy where mail = '%s'));" %('F', fMail, mail))
            self.conn.commit()            
            print('User %s has been successfully added to your friends list!' % (fMail))
        else:            
            print('User does not exist!')
        
    def findFriend(self):
        print('Znalazles')
    
    def logout(self):
        print('Zostales pomyslnie wylogowany')
        
    def deleteAccount():
        print('Konto usuniete pomyslnie')
        
    # TODO: sprawdzanie czy znajmoœæ ju¿ istnieje
    # TODO: DEF KLASA WYSWIETLAJACA twoich znajomych
    # TODO: 3 proby logowania potem wypad
    # TODO: powrot do zamego poczatku po nieudanym logowaniu i po nieudanej rejestracji
    # TODO: po co jest:     def DBclose(self): /         print('Koniec') /         self.conn.close()
    # TODO: klasy testowe i ROZDZIELENIE NA KLASY !!!!!

sql = Projekt('mck')