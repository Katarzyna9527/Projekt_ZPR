/*!
 *  @file   Game.hpp
 *  @brief Header file for Game class of ship game.
 */
#ifndef GAME_HPP
#define GAME_HPP

#include <cstdlib>
#include <iostream>
#include <vector>
#include "State.hpp"
#include "Move.hpp"
#include "Declarations.hpp"

/*!
 *	\brief A class representing Game.
 * It has methods necessery to run and opperate the game. 
 */
class Game{

private:

/*!
 *Pointer to Object of a class Player, representing player with color Blue.
 */
std::shared_ptr<Player> playerBlue_;

/*!
 *Pointer to Object of a class Player, representing player with color Pink.
 */
std::shared_ptr<Player> playerPink_;

/*!
 *Pointer to Object of a class State, representing state of player Blue game.
 */
std::shared_ptr<State> statePlayerBlue_;

/*!
 *Pointer to Object of a class State, representing state of player Pink game.
 */
std::shared_ptr<State> statePlayerPink_;

/*!
 * Method change players turns. Set Player active flag. 
 */
void changePlayer();

public:

/*!
 * Constructor of class Game. Create Object representing players and theirs States.
 */
Game();

/*!
 * @return the Color of this Player which has turn now.
 */
Color whichPlayerNow() const;

/*!
 * method checks if it wasn't the same move erlier.
 * @param move pointer to object Move
 * @return true if move is correct and can be execute 
 */
bool checkMove(std::shared_ptr<Move> move) const; 

/*!
 * method execute the correct move, update board of Player Moves and check if any Ship was hit
 * @param move pointer to object Move
 */
void executeMove(std::shared_ptr<Move> move); //wykonuje ruch ktory juz jest poprawny

/*!
 * method checks if player has won 
 * @param color identify which player must be check, players color
 */
bool checkVictory(const Color& color) const;

/*!
 * method retrun Board of Players ships setting
 * @param color players color, identify which player board to return
 */
Board getBoardOfShipsSettings(const Color& color)const; 

};



#endif // GAME_HPP
