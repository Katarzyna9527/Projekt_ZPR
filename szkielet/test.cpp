#include <boost/test/included/unit_test.hpp>
#include <iostream>
#include "State.hpp"

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

void test_case3(){

	bool **tab = new bool*[10];
	for(int i=0; i<10; i++){
	tab[i] = new bool[10];
	for(int j=0; j<10; j++){
	tab[i][j] = 1;
	}
	}
	tab[0][0] = 0;
	tab[0][1] = 0;
	State *s = new State();
	Location loc = s->findLocation(4,tab);
	std::cout<<"Statek wspolrzedna x = "<<loc.x<<std::endl;
	std::cout<<"Statek wspolrzedna y = "<<loc.y<<std::endl;	
	std::cout<<"Statek direction = "<<loc.direction<<std::endl;		
	BOOST_CHECK_EQUAL(0,0);
}

test_suite* init_unit_test_suite( int argc, char * argv[] )
{
   
	test_suite *ts0 = BOOST_TEST_SUITE( "CheckPlayersSuite" );
	//ts0->add( BOOST_TEST_CASE( & test_case1 ) );
	//ts0->add( BOOST_TEST_CASE( & test_case2 ) );
    ts0->add( BOOST_TEST_CASE( & test_case3 ) );
    
	framework::master_test_suite().add( ts0 );
    return 0;
}
