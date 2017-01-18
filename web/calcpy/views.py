## @file calcpy/views.py
#  @brief calculation library interface to client


import calc
import psycopg2
import version.models

def loginUser(params):
	print "Got name ",params["name"]," password ",params["pass"]
	return { "session-token": 10203 }

class GameStub:
	hit_counter = 0

def userMove(params):
	print "Got move request, token: ",params["token"],", (x,y): (",params["x"],params["y"],")"
	GameStub.hit_counter += 1
	return { "valid": 1, "hit": GameStub.hit_counter%2 }

def getBoards(params): # uwaga odwrocone osie (x/y)
	return { "ships": [[],[None, None, "up", "up", "down"],[],[],[],[],[],[]], "shots": [[],[],[None, "hit"],[],[],[],[],[]], "turn": False }

def loginUser(params):
	print params
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
	cur.execute("SELECT LOGIN,PASSWORD FROM GAME_USERS")
	rows=cur.fetchall()
	for row in rows:
		if row[0]==login and row[1]==password:
			conn.close()
			return 0
	conn.close()
	return 1
		


def registerUser(params):
	conn=psycopg2.connect(database=version.models.getDBNAME(), user=version.models.getDBUser, password=version.models.getDBPassword(), host="127.0.0.1", port="5432")
	cur=conn.cursor()
	cur.execute("SELECT 1 FROM pg_tables WHERE schemaname='public' AND tablename='game_users'")
	rows=cur.fetchall()
	if len(rows)==0:
		cur.execute('''CREATE TABLE GAME_USERS
       		(ID INT PRIMARY KEY    NOT NULL,
       		LOGIN          TEXT    NOT NULL,
       		PASSWORD       TEXT    NOT NULL,
		WINS           INT     NOT NULL,
		LOSES          INT     NOT NULL);''')
		conn.commit()
	cur.execute("SELECT ID,LOGIN FROM GAME_USERS")
	rows=cur.fetchall()
	newId=0
	for row in rows:
		if row[1]==login:
			conn.close()
			return 1
		if row[0]>=newId:
			newId=row[0]+1
	cur.execute("INSERT INTO GAME_USERS (ID,LOGIN,PASSWORD,WINS,LOSES) \ VALUES (%s,%s,%s,0,0)",(newId,newLogin,newPassword))
	conn.commit()
	conn.close()
	return 0

'''
import calc

def getNumber(params):
    """the calculation from C++ library"""
    return {
        "number" : calc.getNumber()
    }

def getCommands(params):
    """return the commands descriptors"""
    cmdmgr = calc.CommandManager()
    ids = cmdmgr.getIds()
    out = dict()
    for i in ids:
        out[int(i)] = { "state" : str(cmdmgr.getState(i)), "progress": float(cmdmgr.getProgress(i)) }
    return out

def startCommand(params):
    """start new tick command"""
    cmdmgr = calc.CommandManager()
    cmd_id = cmdmgr.start()
    return cmd_id
'''
