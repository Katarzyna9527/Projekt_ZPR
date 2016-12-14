#ifndef DECLARATIONS_HPP
#define DECLARATIONS_HPP

#include <string>
#include <vector>
#include <cstdlib>

// variables which represents color of the ship on a board
typedef std::string Color;
const Color CROSS = "blue";
const Color CIRCLE = "pink";
const Color NONE = "";

typedef std::vector<std::vector<Color> > Board;


#endif // PROJECT_DECLARATIONS_HPP
