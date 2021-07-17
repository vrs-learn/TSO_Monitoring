import cx_Oracle

class Database:

    def __init__(self,server,port,instance,user,passw):
        dsn = cx_Oracle.makedsn(server, port, instance)
        conn = cx_Oracle.connect(user,passw,dsn)
        self.cur = conn.cursor()

    def print_output(self):
        for row in self.cur:
            print(row)

    def run_query(self,query):
        self.cur.execute(query)
        self.print_output()
