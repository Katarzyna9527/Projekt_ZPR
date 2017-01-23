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
	#get
    #def test




'''
	##getGame test
    def test01getGame(self):
	params={"game":'New Game',"token":9999}
	name=views.getGame(params)
	self.assertEqual(name['game'],'Game 1')
	self.assertEqual(name['valid'],True)
	##getGames test
    def test02getGames(self):
	params={"game":'Game 1',"token":9998}
	views.getGame(params)
	params={"game":'New Game',"token":9999}
	views.getGame(params)
	views.getGame(params)
	g=views.getGames(params)
	self.assertEqual(g["games"],["Game 1","Game 2","Game 3"])
	##getColors test
    def test03getColors(self):
	params={"game":'Game 1',"token":9999}
	(color, oponent_color) = views.getColors(params['token'] == views.GameList.games[params['game']]["players"]["blue"])
	self.assertEqual(color,calc.Color.BLUE)
	self.assertEqual(oponent_color,calc.Color.PINK)
	##getBoards test
    def test04getBoards(self):
	params={"game":'Game 1',"token":9997}
	b=views.getBoards(params)
	self.assertEqual(b["valid"],False)
	self.assertEqual(b["winner"],None)
	self.assertEqual(b["ships"],None)
	self.assertEqual(b["shots"],None)
	self.assertEqual(b["turn"],False)
	params={"game":'Game 1',"token":9999}
	b=views.getBoards(params)
	self.assertEqual(b["valid"],True)
	self.assertEqual(b["winner"],None)
	self.assertEqual(b["ships"],views.GameList.games[params["game"]]["game"].ships[calc.Color.BLUE])
	self.assertEqual(b["shots"],views.GameList.games[params["game"]]["game"].shots[calc.Color.BLUE])
	self.assertEqual(b["turn"],False)
	params={"game":'Game 1',"token":9998}
	b=views.getBoards(params)
	self.assertEqual(b["valid"],True)
	self.assertEqual(b["winner"],None)
	self.assertEqual(b["ships"],views.GameList.games[params["game"]]["game"].ships[calc.Color.PINK])
	self.assertEqual(b["shots"],views.GameList.games[params["game"]]["game"].shots[calc.Color.PINK])
	self.assertEqual(b["turn"],True)






	conn=psycopg2.connect(database=version.models.getDBName(), user=version.models.getDBUser(), password=version.models.getDBPassword(), host="127.0.0.1", port="5432")
	cur=conn.cursor()
	cur.execute("DELETE FROM game_users WHERE LOGIN='test1'")
	conn.commit()
	conn.close()
'''
