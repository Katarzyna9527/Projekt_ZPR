#ifndef DECLARATIONS_HPP
#define DECLARATIONS_HPP

#include <string>
#include <vector>
#include <cstdlib>
#include <iostream>

const int BOARD_SIZE = 10;

enum Color {PINK,BLUE};
enum Direction {RIGHT,DOWN};

typedef std::vector <std::vector<bool>> Board;

#endif // PROJECT_DECLARATIONS_HPP
