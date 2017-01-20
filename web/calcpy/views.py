## @file calcpy/views.py
#  @brief calculation library interface to client


import psycopg2
import version.models
import threading
import datetime as dt

class GameList:
	cid = 1
	games = {}

class PlayerList:
	players = {}
	def putPlayer(self, name, token):
		players[name] = {"token": token, "expiry": dt.datetime.now() + dt.timedelta(hours=2)}

	def getPlayer(self, name):
		if name not in players.keys():
			return None
		player = players[name]
		if players[name]["expiry"] > dt.datetime.now():
			return None
		players[name]["expiry"] = dt.datetime.now() + dt.timedelta(hours=2)
		return players[name]

class GameStub:
	BOARDSIZE = 10
	def __init__(self):
		self.ships = [[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]
		self.shots = [[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]
		self.ships[3][1] = "up"
		self.ships[4][1] = "up"
		self.ships[5][1] = "down"
		
		self.shots[6][2] = "hit"
		self.shots[6][3] = "miss"
	
class L:
	l=threading.Lock()

def loginUser(params):
	print "Got name ",params["name"]," password ",params["pass"]
	L.l.acquire()
	token=None
	try:
		conn=psycopg2.connect(database=version.models.getDBName(), user=version.models.getDBUser(), password=version.models.getDBPassword(), host="127.0.0.1", port="5432")
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
				PlayerList.putPlayer(params["name"], token)
				token = row[0]
				raise
	finally:
		conn.close()
		L.l.release()
	return { "session-token": token }

def userMove(params):
	print "Got move request, token: ",params["token"],", (x,y): (",params["x"],params["y"],")"
	return { "valid": 1, "hit": 0 }

def getBoards(params): # uwaga odwrocone osie (x/y)
	name = params["game"]
	if name not in GameList.games.keys():
		return {"valid": False}
	game = GameList.games[name]
	player = params["token"]
	if player != game['blue'] and player != game['pink']:
		return {"valid": False}

	return { "ships": game["game"].ships, "shots": game["game"].shots, "turn": True, "winner": None, "valid":True }

def getGames(params):
	return { "games": GameList.games.keys() }

def getGame(params):
	name = params['game']
	if name == 'New Game':
		name = 'Game '+str(GameList.cid)
		GameList.cid += 1
		GameList.games[name] = {'blue': params['token'], 'pink': None, 'game': GameStub()}
	elif name in GameList.games.keys():
		game = GameList.games[name]
		if game["blue"] is None:
			game["blue"] = params['token']
		elif game["pink"] is None:
			game["pink"] = params['token']
		else:
			return { "game": None, "valid": False }
	return { "game": name, "valid": True }

def registerUser(params):
	print "Got name ",params["name"]," password ",params["pass"]
	L.l.acquire()
	token = None
	try:
		conn=psycopg2.connect(database=version.models.getDBName(), user=version.models.getDBUser(), password=version.models.getDBPassword(), host="127.0.0.1", port="5432")
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
			if row[1]==params["name"]:
				raise
			if row[0]>=newId:
				newId=row[0]+1
		cur.execute(("INSERT INTO GAME_USERS (ID,LOGIN,PASSWORD_HASH,WINS,LOSES) VALUES ({},\'{}\',\'{}\',0,0)").format(newId,params["name"],params["pass"]))
		conn.commit()
		token = newId
		PlayerList.putPlayer(params["name"], token)
	finally:
		conn.close()
		L.l.release()
	return { "session-token": token}

