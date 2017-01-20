/*!
 *  @file   Declarations.hpp
 * @brief File contains typedefs and declarations for Ship game project.
 */

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

/*!
 * Variable representing game board size.
 */
const static int BOARD_SIZE = 10;

/*!
 * Enum representing two players Pink and Blue.
 */
enum Color {PINK,BLUE};

/*!
 * Enum representing direction of Ship location.
 */
enum Direction {RIGHT,DOWN};

/*!
 * typedef of bool game board.
 */
typedef std::vector<std::vector<bool>> Board;

#endif // PROJECT_DECLARATIONS_HPP
