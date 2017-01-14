#ifndef PLAYER_HPP
#define PLAYER_HPP

#include "Ship.hpp"

class Player{
public:

Color color_;
bool active_;
std::vector<Ship*> vectorOfShips; 

Player();
Player(Color color, bool active);
bool amIDead();


};

#endif // PLAYER_HPP
