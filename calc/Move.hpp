/*!
 *  @file   Move.hpp
 *  @brief Header file for Move class of Ships game.
 */
#ifndef MOVE_HPP
#define MOVE_HPP

#include "Declarations.hpp"

/*!
 *	\brief A class representing single Move of Player.
 */
class Move{ 
private:

/*!
 *  x coordinate
 */
int x_;

/*!
 *  y coordinate
 */
int y_;

/*!
 *  Color representing which Player was Move
 */
Color color_;

public:

/*!
 *  Constructor of Move class
 *  @param x x_ coordinate
 *  @param y y_ coordinate
 *  @param color color_
 */
Move(int x, int y, Color color) : x_(x), y_(y), color_(color) {}

/*!
 *  method for testing changes Move atributes
 *  @param x x_ coordinate
 *  @param y y_ coordinate
 *  @param color color_
 */
void setMove(int x, int y, Color color){ 
x_ = x; 
y_ = y; 
color_ = color;
};

/*!
 *  @retrurn x_ coordinate
 */
int getX()const {return x_;}

/*!
 *  @retrurn y_ coordinate
 */
int getY()const {return y_;}

/*!
 *  @retrurn color_ of player which was Move
 */
int getColor()const {return color_;}

};


#endif // MOVE_HPP
