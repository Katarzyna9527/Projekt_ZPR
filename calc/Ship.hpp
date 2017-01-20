#ifndef SHIP_HPP
#define SHIP_HPP

#include "Declarations.hpp"

class Ship{
private:

int x_;
int y_;
Direction direction_;
int shipLength_;
bool isAlive_;
bool *damages;

public:

Ship();
Ship(int shipLength);
void setLocation(const int& x, const int& y, const Direction& dir);
int getLength() const {return shipLength_;}
bool isHit(const int& x, const int& y);
void checkIsAlive();
int getX() const {return x_;}
int getY() const {return y_;}
Direction getDirection() const {return direction_;}
bool getIsAlive() const {return isAlive_;}

};




#endif // PROJECT_SHIP_HPP
