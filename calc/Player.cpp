#include "Player.hpp"

Player::Player(Color color, bool active = false) :color_(color), active_(active){

	for(int i=4; i>0; --i){
		for(int j=1; j<=4-i+1; ++j){
		vectorOfShips.push_back(new Ship(i));  
		}
	}

}
bool Player::amIDead(){return true;}
bool Player::isActive(){return active_;}
void Player::setActive(){active_ = !active_;}

