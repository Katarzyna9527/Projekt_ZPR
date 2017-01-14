#ifndef GAME_HPP
#define GAME_HPP


#include <cstdlib>
#include <vector>
#include "Player.hpp"
#include "Move.hpp"
#include "Declarations.hpp"

class Game{
private:

//Board vector of vectors
Board boardPink_;
Board boardBlue_;
Board board_;
Player playerBlue_;
Player playerPink_;
Move move_;

public:

 const int BOARD_SIZE = 10;
 


  Game();
 ~Game();
  void addPlayer(const Player &player);
  void fillBoard(); //ustawianie wszystkich statków na poczatku gry
  Board getBoard(const int &id);
  bool hasPlayer(const int &id);
  bool hasBothPlayers();
  int checkForWinners(); //zwraca id
  void updateBoard();
  void executeMove();
  void setMove();
 
};



#endif // GAME_HPP
