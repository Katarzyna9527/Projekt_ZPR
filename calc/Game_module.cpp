#include "Game.hpp"
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python.hpp>

//using namespace boost::python;

BOOST_PYTHON_MODULE(calc){

	

	boost::python::enum_<Direction>("Direction")
		.value( "RIGHT", RIGHT )
		.value( "DOWN", DOWN )
		;

	boost::python::enum_<Color>("Color")
		.value( "PINK", PINK )
		.value( "BLUE", BLUE )
		;

	boost::python::class_<std::vector <std::vector<bool> > >("Matrix")
		.def(boost::python::vector_indexing_suite<std::vector <std::vector<bool> > >())
		;

	boost::python::class_<std::vector<bool> >("Vector")
		.def(boost::python::vector_indexing_suite<std::vector<bool> >())
		;

	boost::python::class_<Move>("Move",boost::python::init<int,int,Color>())
		;

	
	boost::python::class_<Game>("Game",boost::python::init<>())
		.def("getBoardOfShipsSettings", &Game::getBoardOfShipsSettings)
		.def("whichPlayerNow", &Game::whichPlayerNow)
		.def("checkMove", &Game::checkMove)
		.def("executeMove", &Game::executeMove)
		.def("checkVictory", &Game::checkVictory)
		;	

}
