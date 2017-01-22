## @file calcpy/views.py
#  @brief calculation library interface to client

from calc import *
import psycopg2
import version.models
import threading
import datetime as dt
import hashlib

class Player:	
	def __init__(self, name, token):
		self.name = name
		self.token = token

class GameList:
	cid = 1
	games = {}

def getColors(p_isblue):
	cdict = {True: Color.BLUE, False: Color.PINK}
	return cdict[p_isblue], cdict[p_isblue == False]

def getToken(password, name):
	m = hashlib.md5()
	m.update(str(password)+str(name)+"arydn2")
	return m.hexdigest()

class GameStub:
	BOARDSIZE = 10
	def __init__(self):
		self.game=Game()
		self.ships = {}
		self.shots = {}
		self.last_move_time = dt.datetime.now()
		self.is_over = False
		self.winner = None
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
				token = getToken(str(in_password), str(params["name"]))
	finally:
		conn.close()
		L.l.release()
		return { "session-token": token }

def registerUser(params):
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



def userMove(params):
	print "Got move request, token: ",params["token"],", (x,y): (",params["x"],params["y"],") for game ",params["game"]
	valid=False
	x=int(params["x"])
	y=int(params["y"])
	name = params["game"]
	L.l.acquire()
	try:
		if name in GameList.games.keys():
			game = GameList.games[name]
			player=params["token"]
			if player not in [p.token for p in game["players"].values()]:
				raise
			(color, oponent_color) = getColors(player == game["players"]["blue"].token)
			if game["game"].game.whichPlayerNow() == color:
				m = Move(x, y, color)
				if game["game"].game.checkMove(m):
					game["game"].last_move_time = dt.datetime.now()
					game["game"].game.executeMove(m)
					valid = True
					if game["game"].ships[oponent_color][x][y] == "up":
						game["game"].shots[color][x][y]="hit"
						game["game"].ships[oponent_color][x][y]="down"
					else:
						game["game"].shots[color][x][y] = "miss"
						
	finally:
		L.l.release()
		return { "valid": valid }

def getBoards(params): # uwaga odwrocone osie (x/y)
	name = params["game"]
	valid=False
	winner=None
	ships=None
	shots=None
	turn=False
	time_left="-"
	player = params["token"]
	L.l.acquire()
	try:
		if name in GameList.games.keys():
			game = GameList.games[name]
			if player not in [p.token for p in game["players"].values()]:
				raise
			for p in game["players"]:
				if game["players"][p] is None:
					game["game"].last_move_time = dt.datetime.now()
					raise
			valid=True

			(color, oponent_color) = getColors(player == game["players"]["blue"].token)
			ships = game["game"].ships[color]
			shots = game["game"].shots[color]

			if game["game"].is_over:
				winner = (game["game"].winner == color)

			turning_player = game["game"].game.whichPlayerNow()

			time_left = game["game"].last_move_time - dt.datetime.now() + dt.timedelta(seconds=30)
			if time_left.seconds < 0 or time_left.seconds > 61:
				time_left = "0.0"
				winner = (color != turning_player)
				game["game"].is_over = True
				game["game"].winner = turning_player
			else:
				if turning_player == color:
					turn = True
<<<<<<< a56903d870a5c53ccd59ab3ff165e2e5d2d849c2

				for c in [color, oponent_color]:
					if game["game"].game.checkVictory(c) == True:
						game["game"].is_over = True
						game["game"].winner = c
						winner = (c == turning_player)
						conn=psycopg2.connect(database="mydb",user="mydb",password="mydb",host="127.0.0.1", port="5432")
						cur=conn.cursor()
						cur.execute("SELECT PASSWORD_HASH,LOGIN,WINS,LOSES FROM game_users")
						rows=cur.fetchall()
						for row in rows:
							if getToken(str(row[0]),str(row[1])) == params["token"]:
								winner_color = {Color.BLUE: "blue", Color.PINK: "pink"}[c]
								loser_color = {"pink": "blue", "blue": "pink"}[winner_color]
								loser_login = game["players"][loser_color].login
								winner_login = game["players"][winner_color].login
								if (winner):
									row[2]=int(row[2])+1
									cur.execute(("UPDATE game_users SET WINS={} WHERE LOGIN=\'{}\'").format(row[2],winner_login))
								else:
									row[3]=int(row[3])+1
									cur.execute(("UPDATE game_users SET LOSES={} WHERE LOGIN=\'{}\'").format(row[3],loser_login))
								conn.commit()
								break
						conn.close()
						break
=======
				if game["game"].game.checkVictory(color) == True:
					winner=True
					conn=psycopg2.connect(database="mydb",user="mydb",password="mydb",host="127.0.0.1", port="5432")
					cur=conn.cursor()
					cur.execute("SELECT PASSWORD_HASH,LOGIN,WINS FROM game_users")
					rows=cur.fetchall()
					print "lol"
					for row in rows:
						if getToken(str(row[0]),str(row[1])) == params["token"]:
							row[2]=int(row[2])+1
							cur.execute(("UPDATE game_users SET WINS={} WHERE LOGIN=\'{}\'").format(row[2],row[1]))
							conn.commit()
							break
					print "lol"
					conn.close()
					game["game"].is_over = True
				elif game["game"].game.checkVictory(oponent_color) == True:
					winner=False
					conn=psycopg2.connect(database="mydb",user="mydb",password="mydb",host="127.0.0.1", port="5432")
					cur=conn.cursor()
					cur.execute("SELECT PASSWORD_HASH,LOGIN,LOSES FROM game_users")
					rows=cur.fetchall()
					print "lol"
					for row in rows:
						if getToken(str(row[0]),str(row[1])) == params["token"]:
							row[2]=int(row[2])+1
							cur.execute(("UPDATE game_users SET LOSES={} WHERE LOGIN=\'{}\'").format(row[2],row[1]))
							conn.commit()
							break
					print "lol"
					conn.close()
					game["game"].is_over = True
				ships = game["game"].ships[color]
				shots = game["game"].shots[color]
>>>>>>> znowu testy
	finally:
		L.l.release()
		return { "ships": ships, "shots": shots, "turn": turn, "winner": winner, "valid": valid, "time_left": str(time_left).split(".")[0] }

def getGames(params):
	games = [(game, GameList.games[game]["players"]["blue"].name) for game in GameList.games if (GameList.games[game]["players"]["pink"] is None and not GameList.games[game]["game"].is_over)]
	return { "games": games }

def getGame(params):
	name = params['game']
	valid = False
	L.l.acquire()
	try:
		if name == 'New Game':
			name = 'Game '+str(GameList.cid)
			GameList.cid += 1
			GameList.games[name] = { "players": { 'blue': Player(params['login'], params['token']), 'pink': None }, 'game': GameStub() }
			valid=True
		elif name in GameList.games.keys():
			game = GameList.games[name]
			if game["players"]["blue"].token == params["token"]:
				valid=True
			elif game["players"]["pink"] is None:
				game["players"]["pink"] = Player(params["login"], params["token"])
				valid=True
				game["game"].last_move_time = dt.datetime.now()
	finally:
		L.l.release()
		return { "game": name, "valid": valid }

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
		cur.execute("SELECT PASSWORD_HASH,LOGIN,WINS,LOSES FROM GAME_USERS")
		rows=cur.fetchall()
		for row in rows:
			if getToken(str(row[0]),str(row[1])) == params["token"]:
				ratio=(float(row[2]))/(float(row[3])+float(row[2]))
	finally:
		conn.close()
		L.l.release()
		return { "win_ratio": ratio }

def onPlayerLeave(params):
	token = params['token']
	game = params['game']
	L.l.acquire()
	try:
		print "Player ",token," has left the game ",game,"."
		if game not in GameList.games.keys():
			raise
		if (GameList.games[game]["game"].is_over):
			for color in GameList.games[game]["players"]:
				if GameList.games[game]["players"][color].token == token:
					GameList.games[game]["players"][color] = None
					break
		else:
			for color in GameList.games[game]["players"]:
				for color in ["blue", "pink"]:
					if GameList.games[game]["players"][color] == None:
						del GameList.games[game]

				(color, oponent_color) = getColors(GameList.games[game]["players"]["blue"].token == token)
				GameList.game[game]["game"].is_over = True
				GameList.game[game]["game"].winner = oponent_color
				GameList.game[game]["players"][{Color.BLUE: 'blue', Color.PINK: 'pink'}[color]] = None
	finally:
		L.l.release()
		return {}
