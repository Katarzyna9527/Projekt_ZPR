/*!
 *  @file   Player.cpp
 *  @brief File contains implemented methods of a Player class.
 */
#include "Player.hpp"
Player::Player(Color color, bool active = false) :color_(color), active_(active){

	for(int i=4; i>0; --i){
		for(int j=1; j<=4-i+1; ++j){
		vectorOfShips.push_back(std::make_shared<Ship>(i));  
		}
	}

	victory_=false;

}

bool Player::isActive() const {return active_;}
void Player::setActive() {active_ = !active_;}
bool Player::getVictory() const{return victory_;}
void Player::setVictory() {victory_ = true;}
std::vector<std::shared_ptr<Ship>>::iterator Player::begin() {return vectorOfShips.begin();}
std::vector<std::shared_ptr<Ship>>::iterator Player::end() {return vectorOfShips.end();}
int Player::getVectorSize() const {return vectorOfShips.size();}
