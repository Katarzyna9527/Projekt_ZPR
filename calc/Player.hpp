#ifndef PLAYER_HPP
#define PLAYER_HPP

#include "Ship.hpp"
#include "Declarations.hpp"

class Player{
private:
Color color_;
bool active_;
bool victory_;
std::vector<std::shared_ptr<Ship>> vectorOfShips; 


public:
Player();
Player(Color color, bool active);
bool isActive() const;
void setActive();
bool getVictory() const;
void setVictory();
std::vector<std::shared_ptr<Ship>>::iterator begin();
std::vector<std::shared_ptr<Ship>>::iterator end();
int getVectorSize() const;

};

#endif // PLAYER_HPP
