/*!
 *  @file   State.hpp
 *  @brief Header file for State class of Ship game.
 */
#ifndef STATE_HPP
#define STATE_HPP

#include "Player.hpp"
#include "Declarations.hpp"

/*!
 * Global random generator
 */
static boost::random::mt19937 randGen(std::time(0));

/*!
 *	\brief Struct representing coordinates x,y of Ship to generate random ship position. 
 */
struct Position{
int x,y;
};

/*!
 *	\brief Struct representing Ship location on Board x,y and direction.
 */
struct Location{
int x,y;
Direction direction;
};

/*!
 *	\brief A class representing satate of player game.
 * It contains board od of player's past moves, setting of Ships on Board,
 * Initialize board of Ships before starting game 
 */
class State{
private:

/*!
 * Board representing player's ship setting.
 */
Board stateOfShips;

/*!
 * Board representing all pasts player moves.
 */
Board stateOfMoves;
	
/*!
 *  Method inicializes Board of Ships, finding them random correct location 
 *  @param player is pointer to object Player representing one of Two game Players
 */
void initializeState(std::shared_ptr<Player> player);

/*!
 *  Method find final location for Ship, checking rest of Ship setting on Board
 *  @param length is length of Ship
 *  @param board is a temporary board of forbidden settings 
 *  @retrurn final location of Ship 
 */
Location findLocation(const int& length,const Board& board);

/*!
 *  Method find random direction DOWN or RIGHT to set Ship on board
 *  retrurn direction
 */
Direction randomDirection();

/*!
 *  Method find random position x,y with range appropriate to ship length and direction to set ship on board
 *  @param length is length of Ship
 *  @param dir is Ship direction
 *  retrurn Position
 */
Position randomPosition(const int& length,const Direction& dir);

/*!
 *  Method set single ship on Board and actualize temporary board of forbbiden ship settings
 *  @param ship is a ship to set on board
 *  @param tabOfForbiddenSettings is a temporary board of forbbiden Ship positions
 *  @param loc is final location of ship 
 *  @param length is a ship length
 */
void setShip(std::shared_ptr<Ship> ship, Board& tabofForbiddenPos, const Location& loc, const int& length);


public:

/*!
 *  Constructor of class State initialize Board of Ships and Board of Moves
 *  @param player is pointer to object Player representing one of two game players
 */
State(std::shared_ptr<Player> player);

/*!
 *  Method update boardOfMoves if move was done
 *  @param x x coordinate of a Move
 *  @param y y coorinate of a Move
 */
void updateState(const int& x, const int& y);

/*!
 *  retrurn stateOfShips board
 */
Board getStateOfShips()const {return stateOfShips;}

/*!
 *  retrurn stateOfMoves board
 */
Board getStateOfMoves()const {return stateOfMoves;}

};




#endif // PROJECT_STATE_HPP
