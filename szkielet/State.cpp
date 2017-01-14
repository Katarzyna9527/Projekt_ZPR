#include "State.hpp"

State::State(){
randGen.seed(std::time(0));

}
void State::initializeState(Player &player){

bool tabOfForbidenSettings[BOARD_SIZE][BOARD_SIZE] = {};
	

	for(int i=4; i>0; ++i){
		for(int j=1; j<=4; ++j){
		//setShip(i,tabOfForbidenSettings);
		}	
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

Location State::findLocation(const int& length,bool** begin){
	bool badNumber = true;
	Direction dir;
	Position pos;
	int x,y,i;
	i = length;
	Location location;	
	while(badNumber){
		dir = randomDirection();
		pos = randomPosition(length,dir);
		x = pos.x;
		y = pos.y;
		
			if(x == 0 && y == 0) {i = 0;badNumber = false;}
			/*else
			{
				if(dir == RIGHT)x++;
				else y++;
				if(i == 1) badNumber = false;
				i--;				
			}*/
			
	}
	location.x = pos.x;
	location.y = pos.y;
	location.direction = dir;
		
	return location;
}

void State::updateState(){}	
