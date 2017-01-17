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

bool **stateOfShips;
bool **stateOfMoves;
boost::random::mt19937 randGen;
int z;

State(Player* player);	
void initializeState(Player* player);
void updateState(const int& x, const int& y);
Location findLocation(const int& length,bool** tab);
Direction randomDirection();
Position randomPosition(const int& length,const Direction& dir);
void setShip(Ship* ship, bool** tab, const Location& loc, const int& length);

};




#endif // PROJECT_STATE_HPP
