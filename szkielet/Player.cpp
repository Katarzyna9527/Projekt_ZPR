#include "Player.hpp"

Player::Player(Color color, bool active = false) :color_(color), active_(active){

	for(int i=4; i>0; --i){
		for(int j=1; j<=4; ++j){
		vectorOfShips.push_back(new Ship(0,0,RIGHT,i,true));  
		}
	}

}
bool Player::amIDead(){return true;}
