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


void initializeState(Player* player);
Location findLocation(const int& length,bool** tab);
Direction randomDirection();
Position randomPosition(const int& length,const Direction& dir);
void setShip(Ship* ship, bool** tab, const Location& loc, const int& length);


public:
State(){};
State(Player* player);
void updateState(const int& x, const int& y);

};




#endif // PROJECT_STATE_HPP
