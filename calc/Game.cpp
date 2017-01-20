#include "Game.hpp"

Game::Game(){			

	//randGen.seed(static_cast<unsigned int>(std::time(0)));
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

/*bool** Game::getBoardOfShips(const Color& color){
	if(color == BLUE) return statePlayerBlue_->stateOfShips;
	else return statePlayerPink_->stateOfShips;
}*/


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
			for (auto i = playerPink_->begin() ; i != playerPink_->end();++i)	
			{
				if((*i)->isHit(move->getX(), move->getY())) (*i)->checkIsAlive();
			}		
		}
			
	}
	else {
		statePlayerPink_->updateState(move->getX(), move->getY());
		
		if(statePlayerBlue_->getStateOfShips()[move->getX()][move->getY()] == 1){			
			for (auto i = playerBlue_->begin() ; i != playerBlue_->end();++i)	
			{
				if((*i)->isHit(move->getX(), move->getY())) (*i)->checkIsAlive();
			}		
		}
	}
	
	changePlayer();

}

bool Game::checkVictory(const Color& color) const{
 unsigned int counter = 0;
	
	if(color == BLUE){
		for(auto i = playerPink_->begin() ; i != playerPink_->end();++i){
			if((*i)->getIsAlive() == false)++counter;
		}	
		if(playerPink_->getVectorSize() == counter) return true;
	}
	else{
		for(auto i = playerBlue_->begin() ; i != playerBlue_->end();++i){
			if((*i)->getIsAlive() == false)++counter;
		}	
		if(playerBlue_->getVectorSize() == counter) return true;
	}
	
return false;
}

/*
Board Game::getBoardOfShipsSettings(const Color& color){

Board board;
bool **b ;
b = getBoardOfShips(color);

	for (int i = 0; i < BOARD_SIZE; ++i)
	{
		board.push_back( std::vector<bool>() );
		for (int j = 0; j < BOARD_SIZE; ++j)
			board[i].push_back(b[i][j]);
	}

return board;
}
*/

//Game::~Game(){}

