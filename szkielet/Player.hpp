#ifndef PLAYER_HPP
#define PLAYER_HPP

#include "Ship.hpp"

class Player{
public:

int id_;
std::string name_;
Color color_;
bool victory_;
bool active_;
std::vector<Ship> vectorOfShips; 

 
Player(int id, std::string name, std::string color, bool victory, bool active);
Ship setShip(int length);//funkcja określa położenie nowego statku, działa do skutku


};

#endif // PLAYER_HPP
