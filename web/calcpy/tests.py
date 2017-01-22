## @file calcpy/tests.py
#  @brief c++ calculation library Python API unit testing

import django.test
import calc
import views
import time

class CalcPyLibraryTestCase(django.test.TestCase):
    """integration test, call C++ library interface from Python"""

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

    def test03whichPlayerNow(self):
	g=calc.Game()
	res=g.whichPlayerNow()
	self.assertEqual(res,calc.Color.PINK)
	m=calc.Move(1,1,calc.Color.PINK)
	g.executeMove(m)
	res=g.whichPlayerNow()
	self.assertEqual(res,calc.Color.BLUE)

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
    def test01getGame(self):
	params={"game":'New Game',"token":9999}
	name=views.getGame(params)
	self.assertEqual(name['game'],'Game 1')
	self.assertEqual(name['valid'],True)

    def test02getGames(self):
	params={"game":'Game 1',"token":9998}
	views.getGame(params)
	params={"game":'New Game',"token":9999}
	views.getGame(params)
	views.getGame(params)
	g=views.getGames(params)
	self.assertEqual(g["games"],["Game 1","Game 2","Game 3"])

    def test03getColors(self):
	params={"game":'Game 1',"token":9999}
	(color, oponent_color) = views.getColors(params['token'] == views.GameList.games[params['game']]["players"]["blue"])
	self.assertEqual(color,calc.Color.BLUE)
	self.assertEqual(oponent_color,calc.Color.PINK)

    def test04getBoards(self):
	params={"game":'Game 1',"token":9997}
	g=views.getBoards(params)
	self.assertEqual(g["valid"],False)
	self.assertEqual(g["winner"],None)
	self.assertEqual(g["ships"],None)
	self.assertEqual(g["shots"],None)
	self.assertEqual(g["turn"],False)
	params={"game":'Game 1',"token":9999}
	g=views.getBoards(params)
	self.assertEqual(g["valid"],True)
	self.assertEqual(g["winner"],None)
	self.assertEqual(g["ships"],views.GameList.games[params["game"]]["game"].ships[calc.Color.BLUE])
	self.assertEqual(g["shots"],views.GameList.games[params["game"]]["game"].shots[calc.Color.BLUE])
	self.assertEqual(g["turn"],False)
	params={"game":'Game 1',"token":9998}
	g=views.getBoards(params)
	self.assertEqual(g["valid"],True)
	self.assertEqual(g["winner"],None)
	self.assertEqual(g["ships"],views.GameList.games[params["game"]]["game"].ships[calc.Color.PINK])
	self.assertEqual(g["shots"],views.GameList.games[params["game"]]["game"].shots[calc.Color.PINK])
	self.assertEqual(g["turn"],True)


