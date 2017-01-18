#ifndef GAME_HPP
#define GAME_HPP


#include <cstdlib>
#include <iostream>
#include <vector>
#include "State.hpp"
#include "Move.hpp"
#include "Declarations.hpp"

class Game{

public:

Player* playerBlue_;
Player* playerPink_;
State* statePlayerBlue_;
State* statePlayerPink_;
//Move* move_;

void changePlayer();

public:

Game();
~Game();
 
Color whichPlayerNow();
bool** getBoardOfShips(const Color& color) const;
bool checkMove(Move* move); 
void executeMove(Move* move); //wykonuje ruch ktory juz jest poprawny
bool checkVictory(const Color& color);
Board getBoardOfShipSettings(const Color& color) const; 

};



#endif // GAME_HPP
