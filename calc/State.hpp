#ifndef STATE_HPP
#define STATE_HPP

#include "Player.hpp"
#include "Declarations.hpp"

static boost::random::mt19937 randGen(std::time(0));


struct Position{
int x,y;
};

struct Location{
int x,y;
Direction direction;
};

class State{
private:

Board stateOfShips;
Board stateOfMoves;
	

void initializeState(std::shared_ptr<Player> player);
Location findLocation(const int& length,const Board& board);
Direction randomDirection();
Position randomPosition(const int& length,const Direction& dir);
void setShip(std::shared_ptr<Ship> ship, Board& tabofForbiddenPos, const Location& loc, const int& length);


public:

State(std::shared_ptr<Player> player);
void updateState(const int& x, const int& y);
Board getStateOfShips()const {return stateOfShips;}
Board getStateOfMoves()const {return stateOfMoves;}

};




#endif // PROJECT_STATE_HPP
