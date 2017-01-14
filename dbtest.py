#!/usr/bin/python
import psycopg2
conn=psycopg2.connect(database="mydb",user="mydb",password="mydb",host="127.0.0.1", port="5432")
print "Opened database successfully"

cur=conn.cursor()

"""
cur.execute('''CREATE TABLE COMPANY
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);''')
print "Table created successfully"
conn.commit()
"""

'''
cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )");

cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");

cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");

cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");
conn.commit()
print "Records created successfully";
'''

'''
cur.execute("SELECT id, name, address, salary  from COMPANY")
rows = cur.fetchall()
for row in rows:
   print "ID = ", row[0]
   print "NAME = ", row[1]
   print "ADDRESS = ", row[2]
   print "SALARY = ", row[3], "\n"
print "Operation done successfully";
'''

'''
cur.execute("UPDATE COMPANY SET SALARY=25000.00 WHERE ID=1")
conn.commit()
print "Total number of rows updated :", cur.rowcount
cur.execute("SELECT id, name, address, salary  from COMPANY")
rows = cur.fetchall()
for row in rows:
   print "ID = ", row[0]
   print "NAME = ", row[1]
   print "ADDRESS = ", row[2]
   print "SALARY = ", row[3], "\n"
print "Operation done successfully";
'''

'''
cur.execute("DELETE FROM COMPANY WHERE ID=2;")
conn.commit()
print "Total number of rows deleted :", cur.rowcount
cur.execute("SELECT id, name, address, salary  from COMPANY")
rows = cur.fetchall()
for row in rows:
   print "ID = ", row[0]
   print "NAME = ", row[1]
   print "ADDRESS = ", row[2]
   print "SALARY = ", row[3], "\n"
print "Operation done successfully";
'''

'''
cur.execute("DROP TABLE COMPANY");
conn.commit()
'''

'''
cur.execute("SELECT 1 FROM pg_tables WHERE schemaname='public' AND tablename='company'")
rows=cur.fetchall()
print rows[0]
'''

conn.close()
