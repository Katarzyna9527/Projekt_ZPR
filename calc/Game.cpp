/*!
 *  @file   Game.cpp
 *  @brief File contains implemented methods of a Game class.
 */
#include "Game.hpp"

Game::Game(){			

	playerBlue_ = std::make_shared<Player>(BLUE, false);
	playerPink_ = std::make_shared<Player>(PINK, true);
	statePlayerBlue_ = std::make_shared<State>(playerBlue_);
	statePlayerPink_ = std::make_shared<State>(playerPink_);
}


Color Game::whichPlayerNow() const{
	if(playerBlue_->isActive() == true)return BLUE;
	else return PINK;
}

void Game::changePlayer(){
	playerBlue_->setActive();
	playerPink_->setActive();
}


//sprawdza tylko pole nie sprawdza czy teraz kolej danego gracza
bool Game::checkMove(std::shared_ptr<Move> move) const{

	if(move->getColor() == BLUE && statePlayerBlue_->getStateOfMoves()[move->getX()][move->getY()] == 1)return false; 
	else {	
	if(move->getColor() == PINK && statePlayerPink_->getStateOfMoves()[move->getX()][move->getY()] == 1)return false; 
	else return true;
	}
}

// w grze można najpierw setMove, a potem tu zamiat argumentu funkcji zrobić this do przedyskutowania
void Game::executeMove(std::shared_ptr<Move> move){

	if(move->getColor() == BLUE) {
		statePlayerBlue_->updateState(move->getX(), move->getY());
		if(statePlayerPink_->getStateOfShips()[move->getX()][move->getY()] == 1){			
			for_each(playerPink_->begin(), playerPink_->end(),[&](std::shared_ptr<Ship>& i)	
			{
				if(i->isHit(move->getX(), move->getY())) i->checkIsAlive();
			});		
		}
			
	}
	else {
		statePlayerPink_->updateState(move->getX(), move->getY());
		
		if(statePlayerBlue_->getStateOfShips()[move->getX()][move->getY()] == 1){			
			for_each(playerBlue_->begin(), playerBlue_->end() ,[&](std::shared_ptr<Ship>& i)	
			{
				if(i->isHit(move->getX(), move->getY())) i->checkIsAlive();
			});		
		}
	}
	
	changePlayer();

}

bool Game::checkVictory(const Color& color) const{
  int counter = 0;
	
	auto count_not_alive = [](const std::shared_ptr<Ship>& i){
		return !i->getIsAlive();
	};

	if(color == BLUE){
		counter = count_if(playerPink_->begin(), playerPink_->end(), count_not_alive);	
		if(playerPink_->getVectorSize() == counter){playerBlue_->setVictory(); return true;}
	}
	else{
		counter = count_if(playerBlue_->begin(), playerBlue_->end(), count_not_alive);	
		if(playerBlue_->getVectorSize() == counter){playerPink_->setVictory(); return true;}
	}
	
return false;
}


Board Game::getBoardOfShipsSettings(const Color& color) const{

	if(color == PINK) return statePlayerPink_->getStateOfShips();
	else return statePlayerBlue_->getStateOfShips();
	
}

