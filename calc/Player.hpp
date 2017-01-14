#ifndef PLAYER_HPP
#define PLAYER_HPP

#include "Ship.hpp"

class Player{
public:

int id_;
std::string name_;
Color color_;
bool active_;
std::vector<Ship> vectorOfShips; 

Player();
Player(int id, std::string name, std::string color, bool active);
Ship setShip(int length);//funkcja określa położenie nowego statku, działa do skutku
bool amIDead();


};

#endif // PLAYER_HPP
