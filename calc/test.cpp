#include <boost/test/included/unit_test.hpp>
#include <iostream>
#include "Game.hpp"

using namespace boost::unit_test;

const int Length_4 = 4;
const int Length_2 = 2;

bool checkShip(const int& x, const int& y,const int& length,const Direction& dir,const Board& board){
	for(int i=0; i<length; ++i){
		if(dir == RIGHT && board[x+i][y] == 0)return false;
		if(dir == DOWN && board[x][y+i] == 0)return false;  
	}
return true;
}


bool checkShipSpace(const int& x, const int& y,const int& length,const Direction& dir,const Board& board){
	int xPom = x;	
	int yPom = y;	
	for (int i=0; i<length+2; ++i){
		if(dir == RIGHT){
		xPom =x+i-1;
			if(xPom < BOARD_SIZE && xPom >= 0){
				if(yPom-1>=0) {if(board[xPom][yPom-1]==1){ std::cout<<"1";return false;}}
				if(yPom+1<BOARD_SIZE) {if(board[xPom][yPom+1]==1){std::cout<<"2";return false;}}
			}			
		}
		else{
		yPom =y+i-1;
			if(yPom < BOARD_SIZE && yPom >= 0){
				if(xPom-1>=0) {if(board[xPom-1][yPom]==1){std::cout<<"lol"<<x<<y<<" pom"<<xPom<<yPom<<"length"<<length;return false;}}
				if(xPom+1<BOARD_SIZE) {if(board[xPom+1][yPom]==1){std::cout<<"4";return false;}}
			}
		}	
	}//for
	
	if(dir == RIGHT){
		if(x-1>=0){if(board[x-1][y]==1){std::cout<<"5";return false;}}
		if(x+length<BOARD_SIZE){if(board[x+length][y]==1){std::cout<<"6";return false;}}
	}
	else{
		if(y-1>=0){if(board[x][y-1]==1){std::cout<<"7";return false;}}
		if(y+length<BOARD_SIZE){if(board[x][y+length]==1){std::cout<<"8";return false;}}	
	}
return true;	
	
}

//-------------------------Class_Ship_tests----------------------- 

//constructor test
void test_case1(){
	auto ship = std::make_shared<Ship>(Length_4);
	int length = ship->getLength();
	BOOST_CHECK_EQUAL(length,Length_4);
}

//setLocation funcion test
void test_case2(){
	auto ship = std::make_shared<Ship>(Length_4);
	ship->setLocation(1,2,RIGHT);
	BOOST_CHECK_EQUAL(ship->getX(),1);
	BOOST_CHECK_EQUAL(ship->getY(),2);
	BOOST_CHECK_EQUAL(ship->getDirection(),RIGHT);
}

//isHit function test
void test_case3(){
	auto ship1 = std::make_shared<Ship>(Length_4);
	auto ship2 = std::make_shared<Ship>(Length_2);
	ship1->setLocation(0,0,RIGHT);	
	ship2->setLocation(5,5,DOWN);
	BOOST_CHECK_EQUAL(ship1->isHit(3,0),true);
	BOOST_CHECK_EQUAL(ship2->isHit(5,5),true);
	BOOST_CHECK_EQUAL(ship1->isHit(9,9),false);
}

//checkIsAlive function test
void test_case4(){
	auto ship = std::make_shared<Ship>(Length_4);
	ship->setLocation(0,0,RIGHT);
	ship->isHit(0,0);
	ship->checkIsAlive();
	BOOST_CHECK_EQUAL(ship->getIsAlive(),true);
	ship->isHit(1,0);
	ship->isHit(2,0);
	ship->isHit(3,0);
	ship->checkIsAlive();
	BOOST_CHECK_EQUAL(ship->getIsAlive(),false);
}
//-------------------------Class_Player_tests---------------------------
//constructor function test
void test_case5(){
	auto player = std::make_shared<Player>(PINK,true);
	int numberOfShips = 0;
	for(auto i=player->begin(); i!=player->end(); ++i) ++numberOfShips;
	BOOST_CHECK_EQUAL(numberOfShips,10);
	BOOST_CHECK_EQUAL(player->isActive(),true);
	BOOST_CHECK_EQUAL(player->getVictory(),false);
}

//test setActive function
void test_case6(){
	auto player = std::make_shared<Player>(PINK,true);
	player->setActive();
	BOOST_CHECK_EQUAL(player->isActive(),false);
}

//---------------------Class_Move_tests----------------------------------
//constructor function test
void test_case7(){
	auto move = std::make_shared<Move>(0,0,PINK);
	BOOST_CHECK_EQUAL(move->getX(),0);
	BOOST_CHECK_EQUAL(move->getY(),0);
	BOOST_CHECK_EQUAL(move->getColor(),PINK);
}

//setMove funcion test
void test_case8(){
	auto move = std::make_shared<Move>(0,0,PINK);
	move->setMove(2,5,PINK);
	BOOST_CHECK_EQUAL(move->getX(),2);
	BOOST_CHECK_EQUAL(move->getY(),5);
	BOOST_CHECK_EQUAL(move->getColor(),PINK);
}

//---------------------Class_State_tests--------------------------------
//constructor function test rest method are private
void test_case9(){
	auto player = std::make_shared<Player>(PINK,true);
	auto state = std::make_shared<State>(player);
	int x, y, length;
	Direction dir;
	int shipsOk = 0;
	int shipsSpaceOk = 0;
	for(auto i=player->begin(); i!=player->end(); ++i){
		x = (*i)->getX();
		y = (*i)->getY();
		length = (*i)->getLength();
		dir = (*i)->getDirection();
		if(checkShip(x,y,length,dir,state->getStateOfShips()))++shipsOk;
		if(checkShipSpace(x,y,length,dir,state->getStateOfShips()))++shipsSpaceOk;
	}
	BOOST_CHECK_EQUAL(shipsOk,10);
	BOOST_CHECK_EQUAL(shipsSpaceOk,10);
}
//update state function test
void test_case10(){
	auto player = std::make_shared<Player>(BLUE,true);
	auto state = std::make_shared<State>(player);
	state->updateState(2,5);
	BOOST_CHECK_EQUAL(state->getStateOfMoves()[2][5],1);

}
//---------------------Class_Game_tests----------------------------------
//whichPlayerNow function test
void test_case11(){
	auto game = std::make_shared<Game>();
	BOOST_CHECK_EQUAL(game->whichPlayerNow(),PINK);
}

//executeMove function test
void test_case12(){
	auto game = std::make_shared<Game>();
	auto move = std::make_shared<Move>(1,2,PINK);
	game->executeMove(move);
	BOOST_CHECK_EQUAL(game->whichPlayerNow(),BLUE);
}

//checkMove function test
void test_case13(){
	auto game = std::make_shared<Game>();
	auto move = std::make_shared<Move>(1,2,PINK);
	BOOST_CHECK_EQUAL(game->checkMove(move),true);
	game->executeMove(move);
	BOOST_CHECK_EQUAL(game->checkMove(move),false);
}

//checkVictory function test
void test_case14(){
	auto game = std::make_shared<Game>();
	auto move = std::make_shared<Move>(0,0,PINK);
	BOOST_CHECK_EQUAL(game->checkVictory(PINK),false);
	for(int i=0; i<BOARD_SIZE; ++i){
		for(int j=0; j<BOARD_SIZE; ++j){
			move->setMove(j,i,PINK);
			game->executeMove(move);		
		}
	}
	BOOST_CHECK_EQUAL(game->checkVictory(PINK),true);
}

test_suite* init_unit_test_suite( int argc, char * argv[] )
{
   
	test_suite *ts0 = BOOST_TEST_SUITE( "CheckPlayersSuite" );
	ts0->add( BOOST_TEST_CASE( & test_case1 ) );
	ts0->add( BOOST_TEST_CASE( & test_case2 ) );
   	ts0->add( BOOST_TEST_CASE( & test_case3 ) );
	ts0->add( BOOST_TEST_CASE( & test_case4 ) );
	ts0->add( BOOST_TEST_CASE( & test_case5 ) );   
	ts0->add( BOOST_TEST_CASE( & test_case6 ) );
	ts0->add( BOOST_TEST_CASE( & test_case7 ) );
	ts0->add( BOOST_TEST_CASE( & test_case8 ) );
	ts0->add( BOOST_TEST_CASE( & test_case9 ) );
	ts0->add( BOOST_TEST_CASE( & test_case10 ) );
	ts0->add( BOOST_TEST_CASE( & test_case11 ) );
	ts0->add( BOOST_TEST_CASE( & test_case12 ) );
	ts0->add( BOOST_TEST_CASE( & test_case13 ) );
	ts0->add( BOOST_TEST_CASE( & test_case14 ) );

	framework::master_test_suite().add( ts0 );
    return 0;
}



