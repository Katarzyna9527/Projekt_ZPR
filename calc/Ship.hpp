#ifndef SHIP_HPP
#define SHIP_HPP

#include "Declarations.hpp"

class Ship{
public:

int x_;
int y_;
std::string direction_;
int shipLength_;
bool isAlive_;
bool damages[4];

Ship();
Ship(int x, int y, std::string direction, int shipLength, bool isAlive);

void checkComponentDamages(int x, int y);

};




#endif // PROJECT_SHIP_HPP
