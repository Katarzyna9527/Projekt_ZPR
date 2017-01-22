## @file calcpy/views.py
#  @brief calculation library interface to client

from calc import *
import psycopg2
import version.models
import threading
import datetime as dt
import hashlib

class GameList:
	cid = 1
	games = {}

class PlayerList:
	players = {}

def putPlayer(name, token):
	PlayerList.players[name] = {"token": token, "expiry": dt.datetime.now() + dt.timedelta(hours=2)}

def getPlayer(name):
	retVal=None
	if name in PlayerList.players.keys():
		player = PlayerList.players[name]
		if PlayerList.players[name]["expiry"] <= dt.datetime.now():
			PlayerList.players[name]["expiry"] = dt.datetime.now() + dt.timedelta(hours=2)
			retVal=PlayerList.players[name]
	return retVal

def getColors(p_isblue):
	cdict = {True: Color.BLUE, False: Color.PINK}
	return cdict[p_isblue], cdict[p_isblue == False]

class GameStub:
	BOARDSIZE = 10
	def __init__(self):
		self.game=Game()
		self.ships = {}
		self.shots = {}
		for color in [Color.BLUE, Color.PINK]:
			self.ships[color]=[[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]
			self.shots[color]=[[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]

		m=Matrix()
		v=Vector()
		v[:]=[True,True,True,True,True,True,True,True,True,True]
		m[:]=[v,v,v,v,v,v,v,v,v,v]

		out="BLUE\n"
		m=self.game.getBoardOfShipsSettings(Color.BLUE)
		for i in range(0,GameStub.BOARDSIZE):
			for j in range(0,GameStub.BOARDSIZE):
				if m[i][j]==1:
					self.ships[Color.BLUE][i][j]="up"
					out+="1"
				else:
					out+="0"
			out+="\n"
		out+="PINK\n"
		m=self.game.getBoardOfShipsSettings(Color.PINK)
		for i in range(0,GameStub.BOARDSIZE):
			for j in range(0,GameStub.BOARDSIZE):
				if m[i][j]==1:
					self.ships[Color.PINK][i][j]="up"
					out+="1"
				else:
					out+="0"
			out+="\n"
		print(out)

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
			m = hashlib.md5()
			m.update(str(params["pass"]))
			in_password = m.hexdigest()
			if row[1]==params["name"] and row[2]==in_password:
				m = hashlib.md5()
				m.update(str(params["pass"])+str(params["name"])+"arydn2")
				token = m.hexdigest()
				putPlayer(params["name"], token)
	finally:
		conn.close()
		L.l.release()
		return { "session-token": token }

def userMove(params):
	print "Got move request, token: ",params["token"],", (x,y): (",params["x"],params["y"],") for game ",params["game"]
	valid=False
	hit=False
	x=int(params["x"])
	y=int(params["y"])
	name = params["game"]
	L.l.acquire()
	try:
		if name in GameList.games.keys():
			game = GameList.games[name]
			player=params["token"]
			if player not in game["players"].values():
				raise
			(color, oponent_color) = getColors(player == game["players"]["blue"])
			if game["game"].game.whichPlayerNow() == color:
				m = Move(y, x, color)
				if game["game"].game.checkMove(m):
					game["game"].game.executeMove(m)
					valid = True
					if game["game"].ships[oponent_color][x][y] == "up":
						hit = True
						game["game"].shots[color][x][y]="hit"
						game["game"].ships[oponent_color][x][y]="down"
					else:
						game["game"].shots[color][x][y] = "miss"
						
	finally:
		L.l.release()
		return { "valid": valid, "hit": hit }

def getBoards(params): # uwaga odwrocone osie (x/y)
	name = params["game"]
	valid=False
	winner=None
	ships=None
	shots=None
	turn=False
	player = params["token"]
	L.l.acquire()
	try:
		if name in GameList.games.keys():
			game = GameList.games[name]
			if player not in game["players"].values():
				raise
			(color, oponent_color) = getColors(player == game["players"]["blue"])
			ships = game["game"].ships[color]
			shots = game["game"].shots[color]
			if game["game"].game.checkVictory(color) == True:
				winner=True
			elif game["game"].game.checkVictory(oponent_color) == True:
				winner=False
			if game["game"].game.whichPlayerNow()==color:
				turn=True
			valid=True
	finally:
		L.l.release()
		return { "ships": ships, "shots": shots, "turn": turn, "winner": winner, "valid":valid }

def getGames(params):
	return { "games": GameList.games.keys() }

def getGame(params):
	name = params['game']
	valid = False
	L.l.acquire()
	try:
		if name == 'New Game':
			name = 'Game '+str(GameList.cid)
			GameList.cid += 1
			print(name)
			GameList.games[name] = { "players": { 'blue': params['token'], 'pink': None }, 'game': GameStub() }
			valid=True
		elif name in GameList.games.keys():
			game = GameList.games[name]
			for color in ["blue", "pink"]:
				if (game["players"][color] is None) or (game["players"][color] == params['token']):
					game["players"][color] = params['token']
					valid=True
					break
	finally:
		L.l.release()
		return { "game": name, "valid": valid }

def registerUser(params):
	print "Got name ",params["name"]," password ",params["pass"]
	valid = True
	L.l.acquire()
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
		newId=1
		for row in rows:
			if row[1]==params["name"]: # User is already in the database
				valid = False
				raise
			elif row[0]>=newId:
				newId=row[0]+1
		if valid:
			m = hashlib.md5()
			m.update(str(params["pass"]))
			in_password = m.hexdigest()
			cur.execute(("INSERT INTO GAME_USERS (ID,LOGIN,PASSWORD_HASH,WINS,LOSES) VALUES ({},\'{}\',\'{}\',0,0)").format(newId,params["name"],in_password))
			conn.commit()
	finally:
		conn.close()
		L.l.release()
		if valid:
			return loginUser(params)
		else:
			return { "session-token": None}

def getPlayerInfo(params):
	ratio=0
	L.l.acquire()
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
		cur.execute("SELECT ID,WINS,LOSES FROM GAME_USERS")
		rows=cur.fetchall()
		for row in rows:
			#if row[0]==params["name"]
				ratio=(int(row[1]))/(int(row[2]))
	finally:
		conn.close()
		L.l.release()
		return { "win_ratio": ratio }
