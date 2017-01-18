## @file calcpy/views.py
#  @brief calculation library interface to client


import psycopg2
import version.models

global l=threading.Lock()

def loginUser(params):
	print "Got name ",params["name"]," password ",params["pass"]
	l.acquire()
	conn=psycopg2.connect(database=version.models.getDBNAME(), user=version.models.getDBUser, password=version.models.getDBPassword(), host="127.0.0.1", port="5432")
	cur=conn.cursor()
	cur.execute("SELECT 1 FROM pg_tables WHERE schemaname='public' AND tablename='game_users'")
	rows=cur.fetchall()
	if len(rows)==0:
		cur.execute('''CREATE TABLE GAME_USERS
       		(ID INT PRIMARY KEY     NOT NULL,
       		LOGIN          	TEXT    NOT NULL,
       		PASSWORD_HASH   TEXT    NOT NULL,
		WINS            INT     NOT NULL,
		LOSES           INT     NOT NULL);''')
		conn.commit()
	cur.execute("SELECT ID,LOGIN,PASSWORD_HASH FROM GAME_USERS")
	rows=cur.fetchall()
	for row in rows:
		if row[1]==params["name"] and row[2]==params["pass"]:
			conn.close()
			l.release()
			return { "session-token": row[0] }
	conn.close()
	l.release()
	return { "session-token": None }

def userMove(params):
	print "Got move request, token: ",params["token"],", (x,y): (",params["x"],params["y"],")"
	return { "valid": 1, "hit": 0 }

def getBoards(params): # uwaga odwrocone osie (x/y)
	BOARDSIZE = 10
	ships = [[None for y in range(BOARDSIZE)] for x in range(BOARDSIZE)]
	shots = [[None for y in range(BOARDSIZE)] for x in range(BOARDSIZE)]

	ships[3][1] = "up"
	ships[4][1] = "up"
	ships[5][1] = "down"
	
	shots[6][2] = "hit"
	shots[6][3] = "miss"

	return { "ships": ships, "shots": shots, "turn": True, "winner": None }

def registerUser(params):
	print "Got name ",params["name"]," password ",params["pass"]
	l.acquire()
	conn=psycopg2.connect(database=version.models.getDBNAME(), user=version.models.getDBUser, password=version.models.getDBPassword(), host="127.0.0.1", port="5432")
	cur=conn.cursor()
	cur.execute("SELECT 1 FROM pg_tables WHERE schemaname='public' AND tablename='game_users'")
	rows=cur.fetchall()
	if len(rows)==0:
		cur.execute('''CREATE TABLE GAME_USERS
       		(ID INT PRIMARY KEY    NOT NULL,
       		LOGIN          TEXT    NOT NULL,
       		PASSWORD_HASH  TEXT    NOT NULL,
		WINS           INT     NOT NULL,
		LOSES          INT     NOT NULL);''')
		conn.commit()
	cur.execute("SELECT ID,LOGIN FROM GAME_USERS")
	rows=cur.fetchall()
	newId=0
	for row in rows:
		if row[1]==login:
			conn.close()
			l.release()
			return  { "session-token": None }
		if row[0]>=newId:
			newId=row[0]+1
	cur.execute("INSERT INTO GAME_USERS (ID,LOGIN,PASSWORD_HASH,WINS,LOSES) \ VALUES (%s,%s,%s,0,0)",(newId,params["name"],params["pass"]))
	conn.commit()
	conn.close()
	l.release()
	return { "session-token": newId }

