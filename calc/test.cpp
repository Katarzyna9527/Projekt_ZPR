#include <boost/test/included/unit_test.hpp>
#include <iostream>
#include "Game.hpp"

using namespace boost::unit_test;
/*
void test_case1()
{

	State *s = new State();
	Direction dir1 = s->randomDirection();
	Direction dir2 = s->randomDirection();
	Direction dir3 = s->randomDirection();
	Direction dir4 = s->randomDirection();
	Direction dir5 = s->randomDirection();		
	BOOST_CHECK_EQUAL(dir1,DOWN);
	BOOST_CHECK_EQUAL(dir2,DOWN);
	BOOST_CHECK_EQUAL(dir3,DOWN);
	BOOST_CHECK_EQUAL(dir4,RIGHT);
	BOOST_CHECK_EQUAL(dir5,RIGHT);
}*/

/*
void test_case2()
{
	State *s = new State();
	Position pos = s->random(4,RIGHT);
	std::cout<<"Statek 4 RIGHT wspolrzedna x = "<<pos.x<<std::endl;
	std::cout<<"Statek 4 RIGHT wspolrzedna y = "<<pos.y<<std::endl;
	Position pos1 = s->random(1,DOWN);
	std::cout<<"Statek 1 DOWN wspolrzedna x = "<<pos1.x<<std::endl;
	std::cout<<"Statek 1 DOWN wspolrzedna y = "<<pos1.y<<std::endl;
	Position pos2 = s->random(2,RIGHT);
	std::cout<<"Statek 2 RIGHT wspolrzedna x = "<<pos2.x<<std::endl;
	std::cout<<"Statek 2 RIGHT wspolrzedna y = "<<pos2.y<<std::endl;
	Position pos3 = s->random(3,DOWN);
	std::cout<<"Statek 3 DOWN wspolrzedna x = "<<pos3.x<<std::endl;
	std::cout<<"Statek 3 DOWN wspolrzedna y = "<<pos3.y<<std::endl;		
	BOOST_CHECK_EQUAL(1,1);

}*/
/*
void test_case3(){

	bool **tab = new bool*[10];
	for(int i=0; i<10; i++){
	tab[i] = new bool[10];
	for(int j=0; j<10; j++){
	tab[i][j] = 1;
	}
	}
	tab[0][0] = 0;
	tab[1][0] = 0;
	tab[9][9] = 0;
	State *s = new State();
	Location loc = s->findLocation(1,tab);
	std::cout<<"Statek wspolrzedna x = "<<loc.x<<std::endl;
	std::cout<<"Statek wspolrzedna y = "<<loc.y<<std::endl;	
	std::cout<<"Statek direction = "<<loc.direction<<std::endl;		
	BOOST_CHECK_EQUAL(0,0);
}
*/

/*
void test_case4(){

	bool **tab = new bool*[10];
	for(int i=0; i<10; i++){
	tab[i] = new bool[10];
	for(int j=0; j<10; j++){
	tab[i][j] = 0;
	}
	}
	int shipLength = 2;
	State *s = new State();	
	Ship* ship =new Ship(shipLength);
	Location loc = s->findLocation(shipLength,tab);
	std::cout<<"Statek wspolrzedna x = "<<loc.x<<std::endl;
	std::cout<<"Statek wspolrzedna y = "<<loc.y<<std::endl;	
	std::cout<<"Statek direction = "<<loc.direction<<std::endl;
	s->setShip(ship,tab,loc,shipLength);
	for(int a= 0; a<BOARD_SIZE; a++){
		for(int b=0;b<BOARD_SIZE;b++){	
		std::cout<<s->stateOfShips[b][a]<<" ";
		}
	std::cout<<std::endl;
	}

}*/


/*
void test_case5(){
	Player *player =  new Player(PINK,true);
	State *s = new State();
	s->initializeState(player); 
	for(int a= 0; a<BOARD_SIZE; a++){
		for(int b=0;b<BOARD_SIZE;b++){	
		std::cout<<s->stateOfShips[b][a]<<" ";
		}
	std::cout<<std::endl;
	}
}*/

/*
void test_case6(){
	Game* game = new Game();
	std::cout<<"Aktywny gracz "<< game->whichPlayerNow()<<std::endl;
	game->changePlayer();
	std::cout<<"Aktywny gracz "<< game->whichPlayerNow()<<std::endl;
	game->changePlayer();
	std::cout<<"Aktywny gracz "<< game->whichPlayerNow()<<std::endl;
}
*/
/*
void test_case7(){

	Game* game = new Game();
	bool** tab = game->getBoardOfShips(PINK);
	for(int a= 0; a<BOARD_SIZE; a++){
		for(int b=0;b<BOARD_SIZE;b++){	
		std::cout<<tab[b][a]<<" ";
		}
	std::cout<<std::endl;
	}
	std::cout<<"Aktywny gracz "<< game->whichPlayerNow()<<std::endl;
	game->changePlayer();
	std::cout<<"Aktywny gracz "<< game->whichPlayerNow()<<std::endl;
	game->changePlayer();
	std::cout<<"Aktywny gracz "<< game->whichPlayerNow()<<std::endl;
}*/
/*
void test_case8(){
	int length = 4;
	Ship* ship = new Ship(length);
	ship->setLocation(0,0,RIGHT);
	//std::cout<<ship->isHit(0,0)<<std::endl;
	ship->isHit(0,0);
	ship->isHit(1,0);
	ship->isHit(2,0);
	ship->isHit(3,8);
	ship->isAlive();
	std::cout<<ship->isAlive_<<std::endl;
}*/

void test_case9(){

	Game* game = new Game();
	for(int a= 0; a<BOARD_SIZE; a++){
		for(int b=0;b<BOARD_SIZE;b++){	
		std::cout<<game->statePlayerPink_->stateOfShips[b][a]<<" ";
		}
	std::cout<<std::endl;
	}

	//game->move_->setMove(2,2,BLUE);
	//std::cout<<game->checkMove(game->move_)<<std::endl;
	//game->executeMove(game->move_);
	//std::cout<<"tablica ruchow ruzowego [x][y] ="<<game->statePlayerPink_->stateOfMoves[game->move_->x_][game->move_->y_]<<std::endl;
	//std::cout<<game->checkMove(game->move_)<<std::endl;
	
	

}

test_suite* init_unit_test_suite( int argc, char * argv[] )
{
   
	test_suite *ts0 = BOOST_TEST_SUITE( "CheckPlayersSuite" );
	//ts0->add( BOOST_TEST_CASE( & test_case1 ) );
	//ts0->add( BOOST_TEST_CASE( & test_case2 ) );
   	//ts0->add( BOOST_TEST_CASE( & test_case3 ) );
	//ts0->add( BOOST_TEST_CASE( & test_case4 ) );
	//ts0->add( BOOST_TEST_CASE( & test_case5 ) );   
	//ts0->add( BOOST_TEST_CASE( & test_case6 ) );
	ts0->add( BOOST_TEST_CASE( & test_case9 ) );

	framework::master_test_suite().add( ts0 );
    return 0;
}



