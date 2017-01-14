#ifndef STATE_HPP
#define STATE_HPP

#include "Player.hpp"
#include "Declarations.hpp"
#include "boost/random.hpp"
#include <ctime>

struct Position{
int x,y;
};

struct Location{
int x,y;
Direction direction;
};

class State{
public:

bool stateOfShips[BOARD_SIZE][BOARD_SIZE];
bool stateOfMoves[BOARD_SIZE][BOARD_SIZE];
boost::random::mt19937 randGen;

State();
	
public:

void initializeState(Player &player);
void updateState();
Location findLocation(const int& length,bool** begin);
Direction randomDirection();
Position randomPosition(const int& length,const Direction& dir);
};




#endif // PROJECT_STATE_HPP
