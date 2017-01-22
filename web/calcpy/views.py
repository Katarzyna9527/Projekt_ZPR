## @file calcpy/views.py
#  @brief calculation library interface to client

from calc import *
import psycopg2
import version.models
import threading
import datetime as dt

class GameList:
	cid = 1
	games = {}

class PlayerList:
	players = {}

def putPlayer(name, token):
	PlayerList.players[name] = {"token": token, "expiry": dt.datetime.now() + dt.timedelta(hours=2)}

def getPlayer(name):
	L.l.acquire()
	retVal=None
	try:
		if name in PlayerList.players.keys():
			player = PlayerList.players[name]
			if PlayerList.players[name]["expiry"] <= dt.datetime.now():
				PlayerList.players[name]["expiry"] = dt.datetime.now() + dt.timedelta(hours=2)
				retVal=PlayerList.players[name]
	finally:
		L.l.release()
		return retVal

class GameStub:
	BOARDSIZE = 10
	def __init__(self):
		#self.ships = [[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]
		#self.shots = [[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]		
		self.game=Game()
		self.shipsB=[[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]
		self.shipsP=[[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]
		self.shotsB=[[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]
		self.shotsP=[[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]
		m=Matrix()
		v=Vector()
		v[:]=[True,True,True,True,True,True,True,True,True,True]
		m[:]=[v,v,v,v,v,v,v,v,v,v]
		out="BLUE\n"
		m=self.game.getBoardOfShipsSettings(Color.BLUE)
		for i in range(0,GameStub.BOARDSIZE):
			for j in range(0,GameStub.BOARDSIZE):
				if m[i][j]==1:
					self.shipsB[i][j]="up"
					out+="1"
				else:
					out+="0"
			out+="\n"
		out+="PINK\n"
		m=self.game.getBoardOfShipsSettings(Color.PINK)
		for i in range(0,GameStub.BOARDSIZE):
			for j in range(0,GameStub.BOARDSIZE):
				if m[i][j]==1:
					self.shipsP[i][j]="up"
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
			if row[1]==params["name"] and row[2]==params["pass"]:
				token = row[0]
				putPlayer(params["name"], token)
	finally:
		conn.close()
		L.l.release()
		return { "session-token": token }

def userMove(params):
	print "Got move request, token: ",params["token"],", (x,y): (",params["x"],params["y"],")"
	L.l.acquire()
	valid=0
	hit=0
	print "1"
	x=int(params["x"])
	y=int(params["y"])
	try:
		print "2"
		for name in GameList.games.keys():
			print "3"
			game=GameList.games[name]
			player=params["token"]
			if player == game["blue"]:
				print "blue"
				if game["game"].game.whichPlayerNow()==Color.BLUE and game["game"].shotsB[x][y]==None:
					print "31"
					m=Move(x,y,Color.BLUE)
					if game["game"].game.checkMove(m)==True:
						valid=1
						game["game"].game.executeMove(m)
						print "exec"
						if game["game"].shipsP[x][y]=="up":
							hit=1
							game["game"].shotsB[x][y]=="hit"
							game["game"].shipsP[x][y]=="down"
						else:
							hit=0
							game["game"].shotsB[x][y]=="miss"
				#break
			elif player==game['pink']:
				print "pink"
				if game["game"].game.whichPlayerNow()==Color.PINK: 
					print "31"
					if game["game"].shotsP[x][y]!="miss" and game["game"].shotsP[x][y]!="hit":
						print "32"
						m=Move(y,x,Color.PINK)
						print "33"
						if game["game"].game.checkMove(m)==True:
							print "34"
							game["game"].game.executeMove(m)
							print "exec"
							valid=1
							if game["game"].shipsB[x][y]=="up":
								hit=1
								game["game"].shotsP[x][y]=="hit"
								game["game"].shipsB[x][y]=="down"
							else:
								hit=0
								game["game"].shotsP[x][y]=="miss"
				#break
	finally:
		print "4"
		L.l.release()
		return { "valid": valid, "hit": hit }

def getBoards(params): # uwaga odwrocone osie (x/y)
	name = params["game"]
	valid=False
	winner=None
	ships=[[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]
	shots=[[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]
	turn=False
	player = params["token"]
	L.l.acquire()
	try:
		if name in GameList.games.keys():
			game = GameList.games[name]
			if player == game['blue'] :
				ships=game["game"].shipsB
				shots=game["game"].shotsB
				if game["game"].game.checkVictory(Color.BLUE)==True:
					winner=True
				else:
					winner=False
				if game["game"].game.whichPlayerNow()==Color.BLUE:
					turn=True
				valid=True
			elif player == game['pink']:
				ships=game["game"].shipsP
				shots=game["game"].shotsP
				if game["game"].game.checkVictory(Color.PINK)==True:
					winner=True
				else:
					winner=False
				if game["game"].game.whichPlayerNow()==Color.PINK:
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
			GameList.games[name] = {'blue': params['token'], 'pink': None, 'game': GameStub()}
			valid=True
		elif name in GameList.games.keys():
			game = GameList.games[name]
			if (game["blue"] is None) or (game["blue"] == params['token']):
				game["blue"] = params['token']
				valid=True
			elif (game["pink"] is None) or (game["pink"] == params['token']):
				game["pink"] = params['token']
				valid=True
	finally:
		L.l.release()
		return { "game": name, "valid": valid }

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
		newId=1
		for row in rows:
			if row[1]==params["name"]:
				token=1
			if row[0]>=newId:
				newId=row[0]+1
		if token==None:
			cur.execute(("INSERT INTO GAME_USERS (ID,LOGIN,PASSWORD_HASH,WINS,LOSES) VALUES ({},\'{}\',\'{}\',0,0)").format(newId,params["name"],params["pass"]))
			conn.commit()
			token = newId			
			putPlayer(params["name"], token)
		else:
			token = None
	finally:
		conn.close()
		L.l.release()
		return { "session-token": token}

def getPlayerInfo(params):
	return { "win_ratio": 0.5 }
