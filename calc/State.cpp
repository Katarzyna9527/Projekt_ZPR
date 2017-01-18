#include "State.hpp"

State::State(Player* player){
randGen.seed(std::time(0));
	stateOfShips = new bool*[BOARD_SIZE];
	stateOfMoves = new bool*[BOARD_SIZE];
	for(int i=0; i<BOARD_SIZE; i++){
	stateOfShips[i] = new bool[BOARD_SIZE];
	stateOfMoves[i] = new bool[BOARD_SIZE];
		for(int j=0; j<BOARD_SIZE; j++){
		stateOfShips[i][j] = 0;
		stateOfMoves[i][j] = 0;
		}
	}
	
initializeState(player);

}

void State::initializeState(Player* player){

	Location loc;
	bool **tabOfForbiddenSettings = new bool*[BOARD_SIZE];
	for(int i=0; i<BOARD_SIZE; i++){
	tabOfForbiddenSettings[i] = new bool[BOARD_SIZE];
		for(int j=0; j<BOARD_SIZE; j++){
		tabOfForbiddenSettings[i][j] = 0;
		}
	}
		
		for (std::vector<Ship*>::iterator i = player->vectorOfShips.begin() ; i != player->vectorOfShips.end(); ++i){
		loc = findLocation((*i)->getLength(),tabOfForbiddenSettings);
		setShip(*i,tabOfForbiddenSettings,loc, (*i)->getLength());
		}
	
/*	for(int a= 0; a<BOARD_SIZE; a++){
		for(int b=0;b<BOARD_SIZE;b++){	
		std::cout<<tabOfForbiddenSettings[b][a]<<" ";
		}
	std::cout<<std::endl;
	}
std::cout<<std::endl;
std::cout<<std::endl;
std::cout<<std::endl;
*/
}

Direction State::randomDirection() {
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

Location State::findLocation(const int& length,bool** tab){
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
		std::cout<<"lol"<<std::endl;
		while(fieldFree){
			if(tab[x][y] == 1) {fieldFree = false;}
			else
			{
				if(dir == RIGHT)x++;
				else y++;
				if(i == 1){
					fieldFree = false; 
					badNumber = false;
					break;
				}
				
				i--;				
			}
		}	
	}
	location.x = pos.x;
	location.y = pos.y;
	location.direction = dir;
		
	return location;
}

void State::setShip(Ship* ship, bool** tabOfForbiddenPos, const Location& loc, const int& length){
	
	ship->setLocation(loc.x, loc.y, loc.direction);
	
	for(int i=0; i<length; ++i){
		if(loc.direction == RIGHT){
			stateOfShips[loc.x+i][loc.y] = 1;
			tabOfForbiddenPos[loc.x+i][loc.y] = 1;	
			if(loc.y > 0) tabOfForbiddenPos[loc.x+i][loc.y-1] = 1;
			if(loc.y < BOARD_SIZE-1) tabOfForbiddenPos[loc.x+i][loc.y+1] = 1;
			//if(i == 0 && loc.x > 0) tabOfForbiddenPos[loc.x-1][loc.y] = 1;
			//if(i == length-1 && loc.x+i < BOARD_SIZE-1) tabOfForbiddenPos[loc.x+length][loc.y] = 1;
		}
		else{
			stateOfShips[loc.x][loc.y+i] = 1;
			tabOfForbiddenPos[loc.x][loc.y+i] = 1;	
			if(loc.x > 0)tabOfForbiddenPos[loc.x-1][loc.y+i] = 1;
			if(loc.x < BOARD_SIZE-1)tabOfForbiddenPos[loc.x+1][loc.y+i] = 1;
			//if(i == 0 && loc.y > 0) tabOfForbiddenPos[loc.x][loc.y-1] = 1;
			//if(i == length-1 && loc.y+i < BOARD_SIZE-1) tabOfForbiddenPos[loc.x][loc.y+length] = 1;	
		}	
	}
	
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
	/*
	if(loc.x > 0 && loc.y > 0) tabOfForbiddenPos[loc.x-1][loc.y-1] = 1;
	if(loc.x < BOARD_SIZE && loc.y > 0) tabOfForbiddenPos[loc.x+length-1][loc.y-1] = 1;
	if(loc.x > 0 && loc.y < BOARD_SIZE) tabOfForbiddenPos[loc.x-1][loc.y+1] = 1;
	if(loc.x < BOARD_SIZE && loc.y < BOARD_SIZE) tabOfForbiddenPos[loc.x+length-1][loc.y+1] = 1;
	*/
}

void State::updateState(const int& x, const int& y){
stateOfMoves[x][y] = 1;
}	
