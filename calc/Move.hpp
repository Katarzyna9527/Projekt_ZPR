#ifndef MOVE_HPP
#define MOVE_HPP

#include "Declarations.hpp"

class Move{
private:

int x_;
int y_;
Color color_;

public:
Move(int x, int y, Color color) : x_(x), y_(y), color_(color) {}
void setMove(int x, int y, Color color){ 
x_ = x; 
y_ = y; 
color_ = color;
};
int getX()const {return x_;}
int getY()const {return y_;}
int getColor()const {return color_;}

};


#endif // MOVE_HPP
