/*!
 *  @file   State.cpp
 *  @brief File contains implemented methods of a State class.
 */
#include "State.hpp"

State::State(std::shared_ptr<Player> player){

	for (int i = 0; i < BOARD_SIZE; ++i){
		stateOfMoves.push_back( std::vector<bool>() );
		stateOfShips.push_back( std::vector<bool>() );
		for (int j = 0; j < BOARD_SIZE; ++j){
			stateOfMoves[i].push_back(0);
			stateOfShips[i].push_back(0);
		}//for
	}//for
	
    initializeState(player);
}

void State::initializeState(std::shared_ptr<Player> player){

	Board boardOfForbiddenSettings;
	Location loc;

	for (int i = 0; i < BOARD_SIZE; ++i)
	{
		boardOfForbiddenSettings.push_back( std::vector<bool>() );
		for (int j = 0; j < BOARD_SIZE; ++j)
			boardOfForbiddenSettings[i].push_back(0);
	}


	for (auto i = player->begin() ; i != player->end(); ++i){	
		loc = findLocation((*i)->getLength(),boardOfForbiddenSettings);
		setShip(*i,boardOfForbiddenSettings,loc, (*i)->getLength());
	}
	
}


Direction State::randomDirection(){
	Direction dir;
	boost::random::uniform_int_distribution<> dist(0,1);
	int direction = dist(randGen);
	if(direction)  dir = RIGHT;
	else dir =  DOWN;
	return dir;
}


Position State::randomPosition(const int& length, const Direction& dir){
	Position pos;
	boost::random::uniform_int_distribution<> dist1(0,BOARD_SIZE-1);
	boost::random::uniform_int_distribution<> dist2(0,BOARD_SIZE-length);
	int liczba1 = dist1(randGen);
	int liczba2 = dist2(randGen);
	if(dir==RIGHT)
	{
		pos.x = liczba2;
		pos.y = liczba1;
	}
	else
	{
		pos.x = liczba1;
		pos.y = liczba2;	
	}
	
	return pos;
}

Location State::findLocation(const int& length,const Board& board){
	bool badNumber = true;
	bool fieldFree = true;
	Direction dir;
	Position pos;
	int x,y,i;
	Location location;	
	while(badNumber){
		i = length;
		fieldFree = true;
		dir = randomDirection();
		pos = randomPosition(length,dir);
		x = pos.x;
		y = pos.y;
		while(fieldFree){
			if(board[x][y] == 1) {fieldFree = false;}
			else
			{
				if(dir == RIGHT)x++;
				else y++;
				if(i == 1){
					fieldFree = false; 
					badNumber = false;
					break;
				}//if
				
				i--;				
			}//else
		}//while	
	}//while
	location.x = pos.x;
	location.y = pos.y;
	location.direction = dir;
		
	return location;
}

void State::setShip(std::shared_ptr<Ship> ship, Board& tabOfForbiddenPos, const Location& loc, const int& length){
	
	ship->setLocation(loc.x, loc.y, loc.direction);
	
	//filling tabOfForbidden Positions along the ship length  
	for(int i=0; i<length; ++i){
		if(loc.direction == RIGHT){
			stateOfShips[loc.x+i][loc.y] = 1;
			tabOfForbiddenPos[loc.x+i][loc.y] = 1;	
			if(loc.y > 0) tabOfForbiddenPos[loc.x+i][loc.y-1] = 1;
			if(loc.y < BOARD_SIZE-1) tabOfForbiddenPos[loc.x+i][loc.y+1] = 1;
		}//if
		else{
			stateOfShips[loc.x][loc.y+i] = 1;
			tabOfForbiddenPos[loc.x][loc.y+i] = 1;	
			if(loc.x > 0)tabOfForbiddenPos[loc.x-1][loc.y+i] = 1;
			if(loc.x < BOARD_SIZE-1)tabOfForbiddenPos[loc.x+1][loc.y+i] = 1;	
		}//else	
	}//for
	
	//fiiling tabOfForbidden Positions at the begging and end of Ship
	if(loc.direction == RIGHT){
		if(loc.x > 0){
			tabOfForbiddenPos[loc.x-1][loc.y] = 1;
			if(loc.y > 0)tabOfForbiddenPos[loc.x-1][loc.y-1] = 1;
			if(loc.y < BOARD_SIZE-1)tabOfForbiddenPos[loc.x-1][loc.y+1] = 1;
		}
		if(loc.x+length-1 < BOARD_SIZE-1){
			tabOfForbiddenPos[loc.x+length][loc.y] = 1;
			if(loc.y > 0)tabOfForbiddenPos[loc.x+length][loc.y-1] = 1;
			if(loc.y < BOARD_SIZE-1)tabOfForbiddenPos[loc.x+length][loc.y+1] = 1;	
		}
	}
	else{
		if(loc.y > 0){
			tabOfForbiddenPos[loc.x][loc.y-1] = 1;
			if(loc.x > 0)tabOfForbiddenPos[loc.x-1][loc.y-1] = 1;
			if(loc.x < BOARD_SIZE-1)tabOfForbiddenPos[loc.x+1][loc.y-1] = 1;
			
		}
		if(loc.y+length-1 < BOARD_SIZE-1){
			tabOfForbiddenPos[loc.x][loc.y+length] = 1;
			if(loc.x > 0)tabOfForbiddenPos[loc.x-1][loc.y+length] = 1;
			if(loc.x < BOARD_SIZE-1)tabOfForbiddenPos[loc.x+1][loc.y+length] = 1;
		}	
	}	
	
}

void State::updateState(const int& x, const int& y){
	stateOfMoves[x][y] = 1;
}	


