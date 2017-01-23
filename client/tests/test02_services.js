/// @file test02_services.js
/// @brief client unit tests, check the service calling

var injector = angular.injector(['ng', 'myApp']);
var srv = injector.get('srvInfo')
srv.baseURL = "http://127.0.0.1:50008/"; //port for srv.py mock service

module( "test02_services", {
    setup: function() {
	    this.$scope = injector.get('$rootScope').$new();
    },
    teardown: function() { }
});

function functionResponseCheck(r) {
    //ok( 1 == "1", "function response check");
	ok( typeof(r) != undefined && r.ala == "ala", "srv.py non-empty response testing" );
}

asyncTest( "service getVersion", function() {
    expect( 1 );
	var srv = injector.get('srvInfo');
	srv.getVersion(functionResponseCheck);
    setTimeout(
		function() {
			start();
		},
		100);
});

asyncTest( "service doRegisterUser", function() {
    expect( 1 );
	var srv = injector.get('srvInfo');
	srv.doRegisterUser(functionResponseCheck);
    setTimeout(
		function() {
			start();
		},
		100);
});

asyncTest( "service doUserMove", function() {
    expect( 1 );
	var srv = injector.get('srvInfo');
	srv.doUserMove(functionResponseCheck);
    setTimeout(
		function() {
			start();
		},
		100);
});

asyncTest( "service doGetBoards", function() {
    expect( 1 );
	var srv = injector.get('srvInfo');
	srv.doGetBoards(functionResponseCheck);
    setTimeout(
		function() {
			start();
		},
		100);
});

asyncTest( "service doGetGames", function() {
    expect( 1 );
	var srv = injector.get('srvInfo');
	srv.doGetGames(functionResponseCheck);
    setTimeout(
		function() {
			start();
		},
		100);
});

asyncTest( "service doGetGame", function() {
    expect( 1 );
	var srv = injector.get('srvInfo');
	srv.doGetGame(functionResponseCheck);
    setTimeout(
		function() {
			start();
		},
		100);
});

asyncTest( "service doGetPlayerInfo", function() {
    expect( 1 );
	var srv = injector.get('srvInfo');
	srv.doGetPlayerInfo(functionResponseCheck);
    setTimeout(
		function() {
			start();
		},
		100);
});

asyncTest( "service playerLeft", function() {
    expect( 1 );
	var srv = injector.get('srvInfo');
	srv.playerLeft(functionResponseCheck);
    setTimeout(
		function() {
			start();
		},
		100);
});
