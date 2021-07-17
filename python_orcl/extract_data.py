from db_orcl import Database

user="TSOUSER"
db=Database("clm-pun-026986",1521,"XE","tsouser","changeit")
#q="select * from DBA_USERS where USERNAME = '"+user+"' "

#db.run_query(q)
db.run_query("SELECT * FROM USER_ROLE_PRIVS")
insert_db="INSERT INTO "