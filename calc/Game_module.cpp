#include "Game.hpp"
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python.hpp>

//using namespace boost::python;

BOOST_PYTHON_MODULE(Game_cpp){

	boost::python::enum_<Direction>("Direction")
		.value( "RIGHT", RIGHT )
		.value( "DOWN", DOWN )
		;

	boost::python::enum_<Color>("Color")
		.value( "PINK", PINK )
		.value( "BLUE", BLUE )
		;

	boost::python::class_<Move>("Move",boost::python::init<int,int,Color>())
		;

	
	boost::python::class_<Game>("Game",boost::python::init<>())
		//.def("getBoardOfShips", &Game::getBoardOfShips, boost::python::return_value_policy<boost::python::reference_existing_object>())
		.def("whichPlayerNow", &Game::whichPlayerNow)
		.def("checkMove", &Game::checkMove)
		.def("executeMove", &Game::executeMove)
		.def("checkVictory", &Game::checkVictory)
		;	

}
