import passPackage.keepPass
import pymysql

class sqlConnectionClass:
    
    def __init__(self):
        # set password
        password = passPackage.keepPass.password
        self.conn = pymysql.connect('localhost', 'python_user', password, 'projektt', charset='utf8')
        self.cursor = self.conn.cursor()        
    