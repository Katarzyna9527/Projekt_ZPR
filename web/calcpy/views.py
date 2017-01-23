## @file calcpy/views.py
#  @brief calculation library interface to client

from calc import *
import psycopg2
import version.models
import threading
import datetime as dt
import hashlib

##Class representing a logged in Player.
#It consists of a player's name and token.
class Player:	
	##Constructor of the Player Class
	#@param self The object pointer
	#@param name Name of a newly logged player
	#@param token Token for a newly logged player
	def __init__(self, name, token):
		## Individual name of a logged player
		self.name = name
		## Individual token of a logged player
		self.token = token
		self.wants_replay = False

##Class representing a list of all games existing in the moment.
class GameList:
	##Additional integer used to make name of every game different
	cid = 1
	##Dictionary containing every game currently having place.
	#The name of the game is the key.
	#Under every key there is another dictionary with two keys: "players" and "game".
	#Under "game" key there is GameStub class element representing a game.
	#Under "players" key there is another dictionary consisting of two keys: "blue" and "pink".
	#Under each of the "players" keys there is a Player object representing one of the players taking part in the game.
	games = {}

def getColor(game, token):
	for c in [Color.BLUE, Color.PINK]:
		if game["players"][c] is not None:
			if game["players"][c].token == token:
				return c
	return None

def opositeColor(color):
	return {Color.BLUE: Color.PINK, Color.PINK: Color.BLUE}[color]

##This function return a token value for a chosen Player.
#@param name Name of the chosen Player.
#@param password Password of the chosen Player.
def getToken(password, name):
	m = hashlib.md5()
	m.update(str(password)+str(name)+"arydn2")
	return m.hexdigest()

##Class representing a single game object. 
class GameStub:
	##Size of a game table dimension.
	BOARDSIZE = 10
	##GameStub constructor. Called when creating a new Game on GameList.
	#@param self The GameStub object pointer.
	def __init__(self):
		##Game object from calculation library.
		self.game=Game()
		##Dictionary with two keys: Color.BLUE and Color.PINK.
		#Under each key there is a table containing ships of the game Player marked in the GameList under the corresponding color.
		self.ships = {}
		##Dictionary with two keys: Color.BLUE and Color.PINK.
		#Under each key there is a table containing shots of the game Player marked in the GameList under the corresponding color.
		self.shots = {}
		##Time when player had made his last Move.
		self.last_move_time = dt.datetime.now()
		##Marker representing the end of the Game.
		self.is_over = False
		##Marker representing the color of the Game winner.
		self.winner = None
		for color in [Color.BLUE, Color.PINK]:
			self.ships[color]=[[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]
			self.shots[color]=[[None for y in range(GameStub.BOARDSIZE)] for x in range(GameStub.BOARDSIZE)]

		m=Matrix()
		v=Vector()
		v[:]=[True,True,True,True,True,True,True,True,True,True]
		m[:]=[v,v,v,v,v,v,v,v,v,v]
		#Filling ships tables
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

##Simple mutex class using a threading.lock() mechanism.
class L:
	l=threading.Lock()

##Function for logging in users in the database.
#Returns an individual token of a newly logged Player.
#@param params Dictionary with two keys: "name" and "pass", which represent player's username and password. 
def loginUser(params):
	L.l.acquire()
	token=None
	try:
		conn=psycopg2.connect(database=version.models.getDBName(), user=version.models.getDBUser(), password=version.models.getDBPassword(), host="127.0.0.1", port="5432")
		cur=conn.cursor()
		#check if the database exist and if not create one
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
		#compare name and password with the database
		cur.execute("SELECT ID,LOGIN,PASSWORD_HASH FROM GAME_USERS")
		rows=cur.fetchall()
		for row in rows:
			m = hashlib.md5()
			m.update(str(params["pass"]))
			in_password = m.hexdigest()
			#data correct
			if row[1]==params["name"] and row[2]==in_password:
				token = getToken(str(in_password), str(params["name"]))
	finally:
		conn.close()
		L.l.release()
		return { "session-token": token }
##Function for registering new user into the database.
#Returns token of the newly registered player.
#@param params Dictionary with two keys: "name" and "pass", which represent player's username and password. 
def registerUser(params):
	valid = True
	L.l.acquire()
	try:
		conn=psycopg2.connect(database=version.models.getDBName(), user=version.models.getDBUser(), password=version.models.getDBPassword(), host="127.0.0.1", port="5432")
		cur=conn.cursor()
		#check if the database exist and if not create one
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
			# User is already in the database
			if row[1]==params["name"]: 
				valid = False
				raise
			#generate new id for a new player
			elif row[0]>=newId:
				newId=row[0]+1
		if valid:
			#put new player into database
			m = hashlib.md5()
			m.update(str(params["pass"]))
			in_password = m.hexdigest()
			cur.execute(("INSERT INTO GAME_USERS (ID,LOGIN,PASSWORD_HASH,WINS,LOSES) VALUES ({},\'{}\',\'{}\',0,0)").format(newId,params["name"],in_password))
			conn.commit()
	finally:
		conn.close()
		L.l.release()
		#if registration successful log in user
		if valid:
			return loginUser(params)
		else:
			return { "session-token": None}


##Function that execute move requested by the player.
#@param params Dictionary with four keys: "game","token","x" and "y". They represent a move made by the player marked with "token" in the Game named "game". The coordinates of the shot are "x" and "y".
def userMove(params):
	valid=False
	x=int(params["x"])
	y=int(params["y"])
	name = params["game"]
	L.l.acquire()
	try:
		game = GameList.games[name]
		token = params["token"]
		if token not in [player.token for player in game["players"].values()]:
			raise
		color = getColor(game, token)
		if game["game"].game.whichPlayerNow() == color:
			m = Move(x, y, color)
			if game["game"].game.checkMove(m):
				game["game"].last_move_time = dt.datetime.now()
				game["game"].game.executeMove(m)
				if game["game"].ships[opositeColor(color)][x][y] == "up":
					game["game"].shots[color][x][y]="hit"
					game["game"].ships[opositeColor(color)][x][y]="down"
				else:
					game["game"].shots[color][x][y] = "miss"
				valid = True
	finally:
		L.l.release()
		return { "valid": valid }

def updatePlayerStats(game):
	loser_login = game["players"][opositeColor(game["game"].winner)].name
	winner_login = game["players"][game["game"].winner].name

	conn=psycopg2.connect(database="mydb",user="mydb",password="mydb",host="127.0.0.1", port="5432")
	cur=conn.cursor()
	cur.execute(("UPDATE game_users SET wins = wins + 1 WHERE LOGIN = \'{}\'").format(winner_login))
	conn.commit()
	cur.execute(("UPDATE game_users SET loses = loses + 1 WHERE LOGIN = \'{}\'").format(loser_login))
	conn.commit()
	conn.close()

##This is the main function of the server. 
#It returns table of player's ships, shots, whose turn it is, if there is a winner, and how much time the player has for the move before he/she loses.
#@ param params Dictionary with two keys: "token" and "game", which represent calling player's token and game the player plays. 
def getBoards(params): 
	name = params["game"]
	valid=False
	winner=None
	ships=None
	shots=None
	turn=False
	time_left="-"
	token = params["token"]
	L.l.acquire()
	try:
		game = GameList.games[name]
		if not game["game"].is_over:
			for p in game["players"]:
				if game["players"][p] is None:
					game["game"].last_move_time = dt.datetime.now()
					raise
			if token not in [p.token for p in game["players"].values()]:
				raise

		color = getColor(game, token)
		ships = game["game"].ships[color]
		shots = game["game"].shots[color]

		valid=True

		if game["game"].is_over:
			winner = (game["game"].winner == color)
			raise

		turning_player = game["game"].game.whichPlayerNow()

		time_left = game["game"].last_move_time - dt.datetime.now() + dt.timedelta(seconds=30)
		if time_left.seconds < 0 or time_left.seconds > 61:
			time_left = "0.0"
			game["game"].is_over = True
			game["game"].winner = opositeColor(turning_player)
			updatePlayerStats(game)
			winner = (color == game["game"].winner)
		else:
			if turning_player == color:
				turn = True

			for c in [color, opositeColor(color)]:
				if game["game"].game.checkVictory(c) == True:
					game["game"].is_over = True
					game["game"].winner = c
					updatePlayerStats(game)
					winner = (game["game"].winner == color)
					break
	finally:
		L.l.release()
		return { "ships": ships, "shots": shots, "turn": turn, "winner": winner, "valid": valid, "time_left": str(time_left).split(".")[0] }

##Function returning all of the games (their names and players who are already in) except from full and empty ones
def getGames(params):
	L.l.acquire()
	try:
		games = [(game, GameList.games[game]["players"][Color.BLUE].name) for game in GameList.games if (GameList.games[game]["players"][Color.PINK] is None and not GameList.games[game]["game"].is_over)]
	finally:
		L.l.release()
		return { "games": games }

##Function for adding a player to the game, a new or old one.
#It returns the name of the game.
#@param params Dictionary with three keys: "game", "login" and "token", which represent the game's name and player's username and token. 
def getGame(params):
	name = params['game']
	valid = False
	L.l.acquire()
	try:
		#create new game
		if name == 'New Game':
			name = 'Game '+str(GameList.cid)
			GameList.cid += 1
			GameList.games[name] = { "players": { Color.BLUE: Player(params['login'], params['token']), Color.PINK: None }, 'game': GameStub() }
			valid=True
		#add player to existing game
		elif name in GameList.games.keys():
			game = GameList.games[name]
			if game["game"].is_over:
				pass
			elif game["players"][Color.PINK] is None:
				game["players"][Color.PINK] = Player(params["login"], params["token"])
				valid=True
				game["game"].last_move_time = dt.datetime.now()
	finally:
		L.l.release()
		return { "game": name, "valid": valid }

##Function returning wins/loses ratio of the chosen player.
#@param params Dictionary with only one key: "token" which represent player's individual token. 
def getPlayerInfo(params):
	ratio=0
	L.l.acquire()
	try:
		conn=psycopg2.connect(database=version.models.getDBName(), user=version.models.getDBUser(), password=version.models.getDBPassword(), host="127.0.0.1", port="5432")
		cur=conn.cursor()
		#create database if it doesn't exist
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
		#get the ratio
		for row in rows:
			if getToken(str(row[0]),str(row[1])) == params["token"]:
				ratio=(float(row[2]))/(float(row[3])+float(row[2]))
		conn.close()
	finally:
		L.l.release()
		return { "win_ratio": ratio }

##Function handling Player leaving the Game and deleting the game
#@param params Dictionary with two keys: "token" and "game", which represent player's token and game's name. 
def onPlayerLeave(params):
	token = params['token']
	game = params['game']
	L.l.acquire()
	try:
		if game not in GameList.games.keys():
			pass
		elif (GameList.games[game]["game"].is_over):
			GameList.games[game]["players"][getColor(GameList.games[game], token)] = None
		else:
			if None in [GameList.games[game]["players"][color] for color in [Color.BLUE, Color.PINK]]:
				del GameList.games[game]
			else:
				color = getColor(GameList.games[game], token)
				GameList.games[game]["game"].is_over = True
				GameList.games[game]["game"].winner = opositeColor(color)
				updatePlayerStats(GameList.games[game])
				GameList.games[game]["players"][color] = None
	finally:
		L.l.release()
		return {}

def onReplayRequest(params):
	token = params['token']
	game_name = params['game']
	L.l.acquire()
	try:
		if game_name not in GameList.games.keys():
			pass
		elif (GameList.games[game]["game"].is_over):
			game = GameList.games[game_name]
			color = getColor(game, token)
			if game["players"][opositeColor(color)] is None:
				pass
			else:
				if game["players"][opositeColor(color)].wants_replay:
					blue = game["players"][color.BLUE]
					pink = game["players"][color.PINK]
					del GameList.games[game_name]
					GameList.games[game_name] = { "players": { Color.BLUE: blue, Color.PINK: pink }, 'game': GameStub() }
					game["players"][opositeColor(color)].wants_replay = True
				else:
					game["players"][color].wants_replay = True
	finally:
		L.l.release()
		return {}
