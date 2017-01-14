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

Player playerBlue_;
Player playerPink_;
State statePlayerBlue_;
State statePlayerPink_;

Game();
~Game();
 
private:
	
	
};



#endif // GAME_HPP
