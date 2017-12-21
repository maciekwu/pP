import sqlConnection
class mail:
    
    def __init__(self, mail):
        self.mail = mail
        sqlConnection.sqlConnectionClass.__init__(self)
        while(True):
            print(' _________________')
            print('|     MESSAGES    |')
            print('|_________________|')            
            print('1 - Send messages')
            print('2 - Read messages')
            print('3 - Back to main menu')
            whatToDo = input('Select an option: ')
            
            if(whatToDo == '1'):
                self.sendMessage()
                if (self.break2Loops == True):
                    break
                continue
            
            elif(whatToDo == '2'):
                self.readMessage()
                continue
            
            elif(whatToDo == '3'):
                break
            
            else:
                print('Select again!')
                
                    
    def sendMessage(self):
        break2Loops = False # TODO: Optimize breaking 2 loops at once
        self.break2Loops = break2Loops
        while(True):
            print(' _________________')
            print('|   SEND MESSAGE  |')
            print('|_________________|')            
            print('1 - Send message')
            print('2 - Back to Messages menu')
            print('3 - Back to Main menu')
            whatToDo = input('Select an option: ')
            
            if (whatToDo == '1'):
                # ask for mail of a friend to whom you would like to send a message
                messRecipient = input('Send message to: ')
                # check if provided recipient == logged user
                if (messRecipient == self.mail):
                    print('You can\'t send message to yourself!')
                    continue
                
                # ask db whether provided recipient exists
                self.cursor.execute("select mail from logowanie where mail = '%s';" %(messRecipient))
                # fetch cursor
                isExist = self.cursor.fetchall()
                if (len(isExist) == 0):
                    print('User does not exist.')
                    continue   
                
                # ask db for friends
                self.cursor.execute("select id_friend from relacje where id_user = (select id from uzytkownicy where mail = '%s') and id_friend = (select id from uzytkownicy where mail = '%s');" %(self.mail, messRecipient)) # TODO: change to complex quert to view
                # fetch cursor
                isFriend = self.cursor.fetchall()
                # check if given mail belongs to any of your friends
                # if Y: ask for message content
                if (len(isFriend) != 0 ):               
                    messContent = input('Message (max 100 chars - TEST): ')                
                    # add message, author and recipient to db
                    self.cursor.execute("insert into wiadomosci (tresc, id_user, id_friend) values (SUBSTR('%s', 1, 100), (select id from Uzytkownicy where mail = '%s'), (select id from Uzytkownicy where mail = '%s'));" %(messContent, self.mail, messRecipient))
                    self.conn.commit()
                    print('Message has been sent.')
                    continue
                # if N:    
                else:
                    print('Cannot send a message. You are not a friend of %s.' %(messRecipient)) 
                    continue
            
            elif (whatToDo == '2'):
                break
            
            elif(whatToDo == '3'):
                self.break2Loops = True
                break
            
            else:
                print('Select once again.')
    
    def readMessage(self):
        while(True):
            # ask db for number of new - unreaded messages
            self.cursor.execute("select count(*) from messageauthorread where is_read = '0' and recipient = '%s';" %(self.mail))
            numOfNewMessages = self.cursor.fetchall()            
            print(' ________________________________')
            print('|            MESSAGES           |')
            print('|   You have %s new message(s)  |' %(numOfNewMessages[0]))
            print('|_______________________________|')
            print('1 - New Messages')
            print('2 - Old messages')
            print('3 - Back to Messages Menu')
            whichMessages = input('Select an option: ')            
            if (whichMessages == '1'):                
                # check db for NEW messages
                self.cursor.execute("select author, content from messageauthorread where is_read = '0' and recipient = '%s';" %(self.mail))
                # fetch cursor
                newMessages = self.cursor.fetchall()
                # check if there are any unreaded messages
                # if Y: print them
                if (len(newMessages) != 0 ):
                    # count number of new messages
                    # display number of new messages
                    print('You have %s new message(s):\n___________________.' %(numOfNewMessages[0]))
                    for author, content in newMessages:
                        print('* New message from %s: %s' %(author, content))
                        # mark message as already readed
                        self.cursor.execute("update wiadomosci set is_read = '1' where id_friend = (select id from uzytkownicy where mail = '%s');" %(self.mail))
                        self.conn.commit()
                        continue
                        
                # if N:     
                else:
                    print('You have no new messages')
                    continue
            elif (whichMessages == '2'):
                # check db for old messages
                self.cursor.execute("select author, content from messageauthorread where is_read = '1' and recipient = '%s';" %(self.mail))
                # fecth cursor with old messages
                oldMessages = self.cursor.fetchall()
                # check if there ara any old messages
                if (len(oldMessages) != 0):                       
                    # display old messages 
                    for author, content in oldMessages:
                        print('* Message from %s: %s' %(author, content))
                        continue
                else:
                    print('You have no messages')
                    continue                    
            elif (whichMessages == '3'):
                break
            else:
                print('Select once again.')    
            