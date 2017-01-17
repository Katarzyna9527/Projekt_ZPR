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
Move* move_;

Game();
~Game();
 
Color whichPlayerNow();
void changePlayer();
bool** getBoardOfShips(Color color);
bool checkMove(Move* move);
void executeMove(Move* move);
bool checkVictory(const Color& color);
	
};



#endif // GAME_HPP
