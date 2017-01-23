## @file calcpy/tests.py
#  @brief c++ calculation library Python API unit testing

import django.test
import calc
import views
import time
import psycopg2
import version.models
import hashlib

class CalcPyLibraryTestCase(django.test.TestCase):
    """integration test, call C++ library interface from Python"""
	##checkMove test
    def test01checkMove(self):
	g=calc.Game()
	for x in range(0,10):
		for y in range(0,10):
			m=calc.Move(x,y,calc.Color.PINK)
			res=g.checkMove(m)
			self.assertEqual(res,True)
			m=calc.Move(x,y,calc.Color.BLUE)
			res=g.checkMove(m)
			self.assertEqual(res,True)
	##executeMove test
    def test02executeMove(self):
	g=calc.Game()
	for x in range(0,10):
		for y in range(0,10):
			m=calc.Move(x,y,calc.Color.PINK)
			res=g.checkMove(m)
			self.assertEqual(res,True)
			g.executeMove(m)
			res=g.checkMove(m)
			self.assertEqual(res,False)
			m=calc.Move(x,y,calc.Color.BLUE)
			res=g.checkMove(m)
			self.assertEqual(res,True)
			g.executeMove(m)
			res=g.checkMove(m)
			self.assertEqual(res,False)
	##whichPlayerNow test
    def test03whichPlayerNow(self):
	g=calc.Game()
	res=g.whichPlayerNow()
	self.assertEqual(res,calc.Color.PINK)
	m=calc.Move(1,1,calc.Color.PINK)
	g.executeMove(m)
	res=g.whichPlayerNow()
	self.assertEqual(res,calc.Color.BLUE)
	##getBoardOfShipsSettings test
    def test04getBoardOfShipsSettings(self):
	g=calc.Game()
	v=calc.Vector()
	m1=calc.Matrix()
	v[:]=[True,True,True,True,True,True,True,True,True,True]
	m1[:]=[v,v,v,v,v,v,v,v,v,v]
	m2=m1
	m1=g.getBoardOfShipsSettings(calc.Color.BLUE)
	m2=g.getBoardOfShipsSettings(calc.Color.PINK)
	count1=0
	count2=0
	for x in range(0,10):
		for y in range(0,10):
			count1+=m1[x][y]
			count2+=m2[x][y]
	self.assertEqual(count1,count2)
	self.assertEqual(count1,20)
	self.assertEqual(count2,20)

class CalcPyViewTestCase(django.test.TestCase):
    """module view test"""
	##registerUser test
    def test01registerUser(self):
	params={"name":"test1","pass":"test1"}
	views.registerUser(params)
	conn=psycopg2.connect(database=version.models.getDBName(), user=version.models.getDBUser(), password=version.models.getDBPassword(), host="127.0.0.1", port="5432")
	cur=conn.cursor()
	cur.execute("SELECT PASSWORD_HASH FROM game_users WHERE LOGIN='test1'")
	rows=cur.fetchall()
	self.assertNotEqual(len(rows),0)
	m = hashlib.md5()
	m.update(str(params["pass"]))
	pass1 = m.hexdigest()
	for row in rows:
		self.assertEqual(row[0],pass1)
	conn.commit()
	conn.close()
	##loginUser and getToken test
    def test02loginUser03getToken(self):
	params={"name":"test1","pass":"test1"}
	token1=views.loginUser(params)['session-token']
	m = hashlib.md5()
	m.update(str(params["pass"]))
	pass1 = m.hexdigest()
	token2=views.getToken(pass1,params["name"])
	self.assertEqual(token1,token2)
	#getGame test
    def test04getGame(self):
	params1={"name":"test1","pass":"test1"}
	#params2={"name":"test2","pass":"test2"}
	token1=views.loginUser(params1)['session-token']
	#token2=views.registerUser(params2)['session-token']
	params2={"game":'New Game',"login":"test1","token":token1}
	name=views.getGame(params2)
	self.assertEqual(name['game'],'Game 1')
	self.assertEqual(name['valid'],True)
	#getGames test
    def test05getGames(self):
	params1={"name":"test1","pass":"test1"}
	token1=views.loginUser(params1)['session-token']
	params2={"game":'New Game',"login":"test1","token":token1}
	views.getGame(params2)
	views.getGame(params2)
	g=views.getGames(params1)
	self.assertEqual(g["games"],[("Game 1","test1"),("Game 2","test1"),("Game 3","test1")])
	#opositeColor test
    def test06opositeColor(self):
	self.assertEqual(views.opositeColor(calc.Color.BLUE),calc.Color.PINK)
	self.assertEqual(views.opositeColor(calc.Color.PINK),calc.Color.BLUE)
	#getColor test
    def test07getColor(self):
	params1={"name":"test1","pass":"test1"}
	token1=views.loginUser(params1)['session-token']
	self.assertEqual(views.getColor(views.GameList.games["Game 1"],token1),calc.Color.BLUE)
	#getBoards test
    def test08getBoards(self):
	params1={"name":"test1","pass":"test1"}
	params2={"name":"test2","pass":"test2"}
	token1=views.loginUser(params1)['session-token']
	token2=views.registerUser(params2)['session-token']
	params3={"game":'Game 1',"login":'test2',"token":token2}
	views.getGame(params3)
	params4={"game":'Game 1',"token":token1}
	params5={"game":'Game 1',"token":token2}
	b1=views.getBoards(params4)
	b2=views.getBoards(params5)
	self.assertEqual(b1["winner"],None)
	self.assertEqual(b1["valid"],True)
	self.assertEqual(b1["turn"],False)
	self.assertEqual(b1["ships"],views.GameList.games["Game 1"]["game"].ships[calc.Color.BLUE])
	self.assertEqual(b1["shots"],views.GameList.games["Game 1"]["game"].shots[calc.Color.BLUE])
	self.assertEqual(b2["winner"],None)
	self.assertEqual(b2["valid"],True)
	self.assertEqual(b2["turn"],True)
	self.assertEqual(b2["ships"],views.GameList.games["Game 1"]["game"].ships[calc.Color.PINK])
	self.assertEqual(b2["shots"],views.GameList.games["Game 1"]["game"].shots[calc.Color.PINK])
	#userMove test
    def test09userMove(self):
	params1={"name":"test1","pass":"test1"}
	params2={"name":"test2","pass":"test2"}
	token1=views.loginUser(params1)['session-token']
	token2=views.loginUser(params2)['session-token']
	params3={"game":'Game 1',"token":token2,"x":int(1),"y":int(2)}
	params4={"game":'Game 1',"token":token1}
	params5={"game":'Game 1',"token":token2}
	b01=views.getBoards(params4)
	b02=views.getBoards(params5)
	m1=views.userMove(params3)
	b1=views.getBoards(params4)
	b2=views.getBoards(params5)
	self.assertEqual(m1["valid"],True)
	self.assertEqual(b01["turn"],False)
	self.assertEqual(b02["turn"],True)
	self.assertEqual(b1["turn"],True)
	self.assertEqual(b2["turn"],False)
	#updatePlayerStats and getPlayerInfo test
    def test10updatePlayerStats11getPlayerInfo(self):
	params1={"name":"test1","pass":"test1"}
	params2={"name":"test2","pass":"test2"}
	token1=views.loginUser(params1)['session-token']
	token2=views.loginUser(params2)['session-token']
	views.GameList.games["Game 1"]["game"].is_over=True
	views.GameList.games["Game 1"]["game"].winner=calc.Color.BLUE
	views.updatePlayerStats(views.GameList.games["Game 1"])
	self.assertEqual(views.getPlayerInfo({"token":token1})["win_ratio"],1)
	self.assertEqual(views.getPlayerInfo({"token":token2})["win_ratio"],0)
	#onReplayRequest test
    def test12onReplayRequest(self):
	params1={"name":"test1","pass":"test1"}
	params2={"name":"test2","pass":"test2"}
	token1=views.loginUser(params1)['session-token']
	token2=views.loginUser(params2)['session-token']
	params3={"game":'Game 1',"token":token1}
	params4={"game":'Game 1',"token":token2}
	views.onReplayRequest(params3)
	views.onReplayRequest(params4)
	b1=views.getBoards(params3)
	b2=views.getBoards(params4)
	self.assertEqual(b1["winner"],None)
	self.assertEqual(b1["valid"],True)
	self.assertEqual(b1["turn"],False)
	self.assertEqual(b1["ships"],views.GameList.games["Game 1"]["game"].ships[calc.Color.BLUE])
	self.assertEqual(b1["shots"],views.GameList.games["Game 1"]["game"].shots[calc.Color.BLUE])
	self.assertEqual(b2["winner"],None)
	self.assertEqual(b2["valid"],True)
	self.assertEqual(b2["turn"],True)
	self.assertEqual(b2["ships"],views.GameList.games["Game 1"]["game"].ships[calc.Color.PINK])
	self.assertEqual(b2["shots"],views.GameList.games["Game 1"]["game"].shots[calc.Color.PINK])
	self.assertEqual(b2["shots"],b1["shots"])
	#onPlayerLeave test
    def test13onPlayerLeave(self):
	params1={"name":"test1","pass":"test1"}
	token1=views.loginUser(params1)['session-token']
	g1=views.getGames(params=None)
	self.assertEqual(g1["games"],[("Game 2","test1"),("Game 3","test1")])
	views.onPlayerLeave({"game":'Game 2',"token":token1})
	g1=views.getGames(params=None)
	self.assertEqual(g1["games"],[("Game 3","test1")])
	#to clear database
    def testInf(self):
	del views.GameList
	conn=psycopg2.connect(database=version.models.getDBName(), user=version.models.getDBUser(), password=version.models.getDBPassword(), host="127.0.0.1", port="5432")
	cur=conn.cursor()
	cur.execute("DELETE FROM game_users WHERE LOGIN='test1'")
	cur.execute("DELETE FROM game_users WHERE LOGIN='test2'")
	conn.commit()
	conn.close()

