#include "Ship.hpp"

Ship::Ship(){}
Ship::Ship(int x, int y, std::string direction, int shipLength, bool isAlive = true) : x_(x), y_(y), direction_(direction), shipLength_(shipLength){}
void Ship::checkComponentDamages(int x, int y){}
