#ifndef MOVE_HPP
#define MOVE_HPP

#include "Declarations.hpp"

class Move{
public:

int x_;
int y_;
Color color_;

Move();
Move(int x, int y, Color color) : x_(x), y_(y), color_(color) {}
void setPoint(int x, int y, Color color){ x_ = x; y_ = y; color_ = color;};

};


#endif // MOVE_HPP
