#
# This program checks if there is a TSO environment already configured :

import sqlite3

default_db = "tsoenv.db"

class envDB:

    def __init__(self, db=default_db):
        self.db = db
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS tsoenv (id INTEGER PRIMARY KEY, server VARCHAR NOT NULL, port INTEGER NOT NULL, sec_value NOT NULL CHECK (sec_value IN (0,1)), username TEXT NOT NULL, password VARCHAR NOT NULL, component TEXT NOT NULL CHECK ( component in ('CDP','REPO','RSSO')), s_or_d TEXT NOT NULL)")
        self.conn.commit()

    def insert(self,server,port,sec_value,username,password,component,s_or_d):
        try:
            self.cur.execute("INSERT INTO tsoenv VALUES(NULL,?,?,?,?,?,?,?)",(server,port,sec_value,username,password,component,s_or_d))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Data Integrity Check failed. " + str(e))
            sys.exit()
        self.cur.execute("SELECT * FROM tsoenv")

    def view(self,component,s_or_d):
        self.cur.execute("SELECT * FROM tsoenv where component=? and s_or_d=?",(component,s_or_d))
        rows=self.cur.fetchall()
        if len(rows) > 0:
            rows=rows[0]
            #rows = c.fetchone()
            if len(rows) == 8:
                data={'id' : rows[0] , 'server' : rows[1] , 'port' : rows[2] , 'sec_value' : rows[3] , 'username' : rows[4] , 'password' : rows[5] , 'component' : rows[6] , 's_or_d' : rows[7]}
                return data
            else :
                return {}
        else :
            return {}

    def delete(self,id):
        self.cur.execute("DELETE FROM tsoenv where id=?",(id))
        self.conn.commit()

    def delete_all(self):
        self.cur.execute("DELETE FROM tsoenv")
        self.cur.execute("SELECT * FROM tsoenv")
        print(self.cur.fetchall())
        self.conn.commit()

    def __del__(self):
        self.conn.close()


'''
database = Database()
try :
    database.insert("clm-aus-018786",38080,0,"aoadmin","admin123","CDP","source")
except sqlite3.IntegrityError as e:
    print("Data Integrity Check failed. " + str(e))

print("The List of enteries in DB are :")
rows=database.view("CDP","source")
print("http://"+str(rows['server'])+":"+str(rows['port']))
print(len(rows))
'''
