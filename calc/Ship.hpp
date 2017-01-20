/*!
 *  @file   Ship.hpp
 *  @brief Header file for class representing Ship.
 */
#ifndef SHIP_HPP
#define SHIP_HPP

#include "Declarations.hpp"

/*
 *  \brief Class represents Ship.
 */
class Ship{
private:

/*!
 *  x coordinate of first segment of Ship
 */
int x_;

/*!
 *  y coordinate of first segment of Ship
 */
int y_;

/*!
 *  direction of Ship, can be DOWN or RIGHT
 */
Direction direction_;

/*!
 *  length of Ship can be 1,2,3,4
 */
int shipLength_;

/*!
 *  flag is false when Ship has Sank
 */
bool isAlive_;

/*!
 *  vector of component damages, size = length of Ship 
 */
std::vector<bool> damages;

public:

/*!
 *  Constructor of a Ship class.
 *  @param shipLength Ship shipLength_
 */
Ship(int shipLength);

/*!
 *  Method set Ship in place of x, y in direction dir at Board of Ships
 *  @param x - Ship x_
 *  @param y - Ship y_
 *  @param dir - Ship direction_
 */
void setLocation(const int& x, const int& y, const Direction& dir);

/*!
 *  @retrurn shipLength_
 */
int getLength() const {return shipLength_;}

/*!
 *  Method check if Ship was hit by executing the Move of x, y coordinate
 *  @param x x coordinate of a Move
 *  @param y y cooridinate of a Move
 *  @retrurn true if Ship was hit
 */
bool isHit(const int& x, const int& y);

/*!
 *  Method check if Ship was sank, If was sank set flag isAlive_ to false 
 */
void checkIsAlive();

/*!
 *  @retrurn x_
 */
int getX() const {return x_;}

/*!
 *  @retrurn y_
 */
int getY() const {return y_;}

/*!
 *  @retrurn direction_
 */
Direction getDirection() const {return direction_;}

/*!
 *  @retrurn isAlive_
 */
bool getIsAlive() const {return isAlive_;}

};




#endif // PROJECT_SHIP_HPP
