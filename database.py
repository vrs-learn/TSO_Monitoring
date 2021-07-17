#
# This program checks if there is a TSO environment already configured :
import sys
import sqlite3

default_db = "tsohealth.db"

class Database:

    def __init__(self, db=default_db):
        self.db = db
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS tsostats (id INTEGER PRIMARY KEY, server VARCHAR NOT NULL, threads INTEGER NOT NULL, max_mem INTEGER NOT NULL , total_mem INTEGER NOT NULL, avail_mem INTEGER NOT NULL, used_mem INTEGER NOT NULL, vm_uptime TEXT NOT NULL, stat_time DATETIME DEFAULT(datetime(CURRENT_TIMESTAMP, 'localtime')) )")
        self.conn.commit()

    def insert(self,server,threads,max_mem,total_mem,avail_mem,used_mem,vm_uptime):
        try:
            self.cur.execute("INSERT INTO tsostats(id,server,threads,max_mem,total_mem,avail_mem,used_mem,vm_uptime) VALUES(NULL,?,?,?,?,?,?,?)",(server,threads,max_mem,total_mem,avail_mem,used_mem,vm_uptime,))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Data Integrity Check failed. " + str(e))
            sys.exit()
        self.cur.execute("SELECT * FROM tsostats")

    def view(self,server):
        self.cur.execute("SELECT * FROM tsostats where server='"+server+"'")
        rows=self.cur.fetchall()
        return rows

    def select_query(self,query):
        self.cur.execute(query)
        rows=self.cur.fetchall()
        return rows

    def delete(self,id):
        self.cur.execute("DELETE FROM tsostats where id=?",(id))
        self.conn.commit()

    def delete_all(self):
        self.cur.execute("DELETE FROM tsostats")
        self.cur.execute("SELECT * FROM tsostats")
        print(self.cur.fetchall())
        self.conn.commit()

    def __del__(self):
        self.conn.close()
