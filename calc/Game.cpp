#include "Game.hpp"

Game::Game(){		

	playerBlue_ = new Player(BLUE, false);
	playerPink_ = new Player(PINK, true);
	statePlayerBlue_ = new State(playerBlue_);
	statePlayerPink_ = new State(playerPink_);
}

Color Game::whichPlayerNow(){
	if(playerBlue_->isActive() == true)return BLUE;
	else return PINK;
}

void Game::changePlayer(){
	playerBlue_->setActive();
	playerPink_->setActive();
}

bool** Game::getBoardOfShips(const Color& color){
	if(color == BLUE) return statePlayerBlue_->stateOfShips;
	else return statePlayerPink_->stateOfShips;
}

/*
Board getBoardOfShipSettings(const Color& color) const{

Board board;

for(int i=0; i<BOARD_SIZE; ++i){
	for(int j=0; j<BOARD_SIZE; ++j)
	{
		board[i][j] = this->getBoardOfShips(color)[i][j]; 
	}
return board;
}

return board;

}
*/

//sprawdza tylko pole nie sprawdza czy teraz kolej danego gracza
bool Game::checkMove(Move* move){

	if(move->getColor() == BLUE && statePlayerBlue_->stateOfMoves[move->getX()][move->getY()] == 1)return false; 
	else {	
	if(move->getColor() == PINK && statePlayerPink_->stateOfMoves[move->getX()][move->getY()] == 1)return false; 
	else return true;
	}
}

// w grze można najpierw setMove, a potem tu zamiat argumentu funkcji zrobić this do przedyskutowania
void Game::executeMove(Move* move){

	if(move->getColor() == BLUE) {
		statePlayerBlue_->updateState(move->getX(), move->getY());
		if(statePlayerPink_->stateOfShips[move->getX()][move->getY()] == 1){			
			for (std::vector<Ship*>::iterator i = playerPink_->vectorOfShips.begin() ; i != playerPink_->vectorOfShips.end();++i)	
			{
				if((*i)->isHit(move->getX(), move->getY())) (*i)->isAlive();
			}		
		}
			
	}
	else {
		statePlayerPink_->updateState(move->getX(), move->getY());
		
		if(statePlayerBlue_->stateOfShips[move->getX()][move->getY()] == 1){			
			for (std::vector<Ship*>::iterator i = playerBlue_->vectorOfShips.begin() ; i != playerBlue_->vectorOfShips.end();++i)	
			{
				if((*i)->isHit(move->getX(), move->getY())) (*i)->isAlive();
			}		
		}
	}
	
	changePlayer();

}

bool Game::checkVictory(const Color& color){
 unsigned int counter = 0;
	
	if(color == PINK){
		for(std::vector<Ship*>::iterator i = playerPink_->vectorOfShips.begin() ; i != playerPink_->vectorOfShips.end();++i){
			if((*i)->isAlive_ == false)++counter;
		}	
		if(playerPink_->vectorOfShips.size() == counter) return true;
	}
	else{
		for(std::vector<Ship*>::iterator i = playerBlue_->vectorOfShips.begin() ; i != playerBlue_->vectorOfShips.end();++i){
			if((*i)->isAlive_ == false)++counter;
		}	
		if(playerBlue_->vectorOfShips.size() == counter) return true;
	}
	
return false;
}

Game::~Game(){}

