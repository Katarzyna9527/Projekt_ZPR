#ifndef GAME_HPP
#define GAME_HPP


#include <cstdlib>
#include <iostream>
#include <vector>
#include "State.hpp"
#include "Move.hpp"
#include "Declarations.hpp"

class Game{

private:

std::shared_ptr<Player> playerBlue_;
std::shared_ptr<Player> playerPink_;
std::shared_ptr<State> statePlayerBlue_;
std::shared_ptr<State> statePlayerPink_;

void changePlayer();

public:

Game();
 
Color whichPlayerNow() const;
//bool** getBoardOfShips(const Color& color);
bool checkMove(std::shared_ptr<Move> move) const; 
void executeMove(std::shared_ptr<Move> move); //wykonuje ruch ktory juz jest poprawny
bool checkVictory(const Color& color) const;
//Board getBoardOfShipsSettings(const Color& color)const; 

};



#endif // GAME_HPP
