/*!
 *  @file   Ship.cpp
 *  @brief File contains implemented methods of a Ship class.
 */
#include "Ship.hpp"

Ship::Ship(int shipLength) : shipLength_(shipLength){
	x_ = 0;
	y_ = 0;
	direction_ = RIGHT;
	isAlive_ = true;
	for(int i=0; i<shipLength; ++i) damages.push_back(0);
}

void Ship::setLocation(const int& x, const int& y, const Direction& dir){
	x_ = x;
	y_ = y;
	direction_ = dir;
}

bool Ship::isHit(const int& x, const int& y){
	for(int i=0; i<shipLength_; ++i){
		if(direction_ == RIGHT){
			if(x_+i == x && y_ == y){
				damages[i] = 1;
				return true;
			}//if
		}//if
		else{
			if(x_ == x && y_+i == y){
				damages[i] = 1;
				return true;
			}//if	
		}//if
	}//for
	return false;
}

void Ship::checkIsAlive(){
	int counter = 0;
	for(int i=0; i<shipLength_; ++i){
		if(damages[i] == 1) ++counter;
	}//for
	if(counter == shipLength_) isAlive_ = false;

}

