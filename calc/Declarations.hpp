#ifndef DECLARATIONS_HPP
#define DECLARATIONS_HPP

#include <string>
#include <vector>
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include <memory>
#include "boost/random.hpp"
#include <ctime>

const static int BOARD_SIZE = 10;
//static boost::random::mt19937 randGen;

enum Color {PINK,BLUE};
enum Direction {RIGHT,DOWN};

typedef std::vector<std::vector<bool>> Board;

#endif // PROJECT_DECLARATIONS_HPP
