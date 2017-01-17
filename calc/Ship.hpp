#ifndef SHIP_HPP
#define SHIP_HPP

#include "Declarations.hpp"

class Ship{
public:

int x_;
int y_;
Direction direction_;
int shipLength_;
bool isAlive_;
bool *damages;

Ship();
Ship(int shipLength);


void setLocation(const int& x, const int& y, const Direction& dir);
int getLength(){return shipLength_;}
bool isHit(const int& x, const int& y);
void isAlive();

};




#endif // PROJECT_SHIP_HPP
