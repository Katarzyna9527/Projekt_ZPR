#include <boost/python.hpp>
#include "Game.hpp"

using namespace boost::python;

BOOST_PYTHON_MODULE(cppGame){
	
	enum_<Color>("Color")
		.value( "PINK", PINK )
		.value( "BLUE", BLUE )
	;

	enum_<Direction>("Direction")
		.value( "LEFT", LEFT )
		.value( "DOWN", DOWN )
	;

	boost::python::class_<Move>("Move")
		.def_readwrite("x", &Move::x_)
		.def_readwrite("y", &Move::y_)
		.def_readwrite("sign", &Move::sign_)
		;

}
