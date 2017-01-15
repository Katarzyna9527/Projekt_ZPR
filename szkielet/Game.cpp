#include "Game.hpp"

Game::Game(){		

	playerBlue_ = new Player(BLUE, false);
	playerPink_ = new Player(PINK, true);
	statePlayerBlue_ = new State(playerBlue_);
	statePlayerPink_ = new State(playerPink_);
	move_ = new Move();
}

Color Game::whichPlayerNow(){
	if(playerBlue_->isActive() == true)return BLUE;
	else return PINK;
}

void Game::changePlayer(){
	playerBlue_->setActive();
	playerPink_->setActive();
}

bool** Game::getBoardOfShips(Color color){
	if(color == BLUE) return statePlayerBlue_->stateOfShips;
	else return statePlayerPink_->stateOfShips;
}

//sprawdza tylko pole nie sprawdza czy teraz kolej danego gracza
bool Game::checkMove(Move* move){

	if(move->color_ == BLUE && statePlayerBlue_->stateOfMoves[move->x_][move->y_] == 1)return false; 
	else {	
	if(move->color_ == PINK && statePlayerPink_->stateOfMoves[move->x_][move->y_] == 1)return false; 
	else return true;
	}
}

// w grze można najpierw setMove, a potem tu zamiat argumentu funkcji zrobić this do przedyskutowania
void Game::executeMove(Move* move){
	if(move->color_ == BLUE) {
		statePlayerBlue_->updateState(move->x_, move->y_);
		if(statePlayerPink_->stateOfShips[move->x_][move->y_] == 1){			
			for (std::vector<Ship*>::iterator i = playerPink_->vectorOfShips.begin() ; i != playerPink_->vectorOfShips.end();++i)	
			{
				if((*i)->isHit(move->x_, move->y_)) (*i)->isAlive();
			}		
		}
			
	}
	else {
		statePlayerPink_->updateState(move->x_, move->y_);
		
		if(statePlayerBlue_->stateOfShips[move->x_][move->y_] == 1){			
			for (std::vector<Ship*>::iterator i = playerBlue_->vectorOfShips.begin() ; i != playerBlue_->vectorOfShips.end();++i)	
			{
				if((*i)->isHit(move->x_, move->y_)) (*i)->isAlive();
			}		
		}
	}
	

}

bool Game::checkVictory(Color color){
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

