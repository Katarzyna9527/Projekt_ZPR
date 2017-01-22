/*!
 *  @file   Player.hpp
 *  @brief Header file for class representing Player.
 */
#ifndef PLAYER_HPP
#define PLAYER_HPP

#include "Ship.hpp"
#include "Declarations.hpp"

/*!
 *  \brief Class represents Player.
 */
class Player{

private:

/*!
 *   Color identyficize Player.
 */
Color color_;

/*!
 *   Is players turn or not.
 */
bool active_;

/*!
 *   Has Player won or not.
 */
bool victory_;

/*!
 *   Vector of Player's ships.
 */
std::vector<std::shared_ptr<Ship>> vectorOfShips; 


public:

/*!
 *  Constructor of a Player class.
 *  @param color Player's color
 *  @param active is Player turn
 */
Player(Color color, bool active);

/*!
 *  @return is Player turn now or not.
 */
bool isActive() const;

/*!
 *  method set Player has turn or not.
 */
void setActive();

/*!
 *  @return victory
 */
bool getVictory() const;

/*!
 *  method set victory
 */
void setVictory();

/*!
 *  @return iterator at first element in vector of Player's ships.
 */
std::vector<std::shared_ptr<Ship>>::iterator begin();

/*!
 *  @return iterator at end of vector of Player's ships. 
 */
std::vector<std::shared_ptr<Ship>>::iterator end();

/*!
 *  @return size of vector of Players'ships.
 */
int getVectorSize() const;

};

#endif // PLAYER_HPP
