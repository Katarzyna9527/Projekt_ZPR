/// @file controllers.js
/// @brief AngularJS controllers

angular.module('myAppControllers', [])
	.controller('loginController',
				['$scope',
				 '$location',
				 'srvInfo',
				 function($scope, $location, srvInfo) {
					 /// Login success handler
					 /// @param data - dictionary holding a token (null if login failed)
					 var callback = function (data) { if (data.data["session-token"]) { token = data.data["session-token"]; $location.path('/list').search('token',token).search('login',$scope.account_name); } else { $scope.login_failed = true; }};
					 var fallback = function () { console.log("Login failed"); $scope.login_failed = true; };

					 $scope.login_failed = false;
					 var token = -1;

					 /// Login handler
					 $scope.on_submit_login = function() {
						 srvInfo.doLoginUser(callback, fallback, $scope.account_name, $scope.account_password);
					 };

					 /// Register handler
					 $scope.on_submit_register = function() {
						 srvInfo.doRegisterUser(callback, fallback, $scope.account_name, $scope.account_password);
					 };

				 }])
	.controller('gameController',
				['$scope',
				 '$timeout',
				 '$routeParams',
				 'srvInfo',
					function($scope, $timeout, $routeParams, srvInfo) {
						 $scope.shiplist = [[],[],[],[],[],[],[],[],[],[]];
						 $scope.shotlist = [[],[],[],[],[],[],[],[],[],[]];
						 var token = $routeParams['token'];
						 var login = $routeParams['login'];
						 $scope.game = $routeParams['game'];
						 $scope.won = null
						 $scope.time_left = "-";

						 $scope.turn = true;
						 /// Gamecell click handler
						 /// @param xpos - x coordinate
						 /// @param ypos - y coordinate
						 $scope.clicked_gamecell = function (xpos, ypos) {
							 if ($scope.shotlist[xpos][ypos]) { console.log("Cannot shoot there"); return; }
							 if ($scope.turn == false) { console.log("Not your turn"); return; }

							 $timeout.cancel($scope.timeout_promise);

							 /// Move success handler
							 /// @param data - holds information whether the move was valid
							 var move_handler = function(data) { 
								 if (data.data["valid"] != 1) { 
									 return;
								 }
								 $scope.timeout_promise = $timeout(refresh, 0);
							 };

							 srvInfo.doUserMove(move_handler, function() {}, xpos, ypos, token, $scope.game);
						 };


						 /// Update boards handler
						 /// @params data - holds information about the board (ships, shots), winners (true - game won, false - game lost, null - game not yet over), time left for player to submit move (time_left)
						 var get_boards_handler = function(data) {
							console.log(data);
								
							$scope.timeout_promise = $timeout(refresh, $scope.REFRESH_INTERVAL);

							$scope.turn = false;
							if (data.data["valid"] === false) {
								return;
							}

							$scope.won = data.data["winner"];
							$scope.time_left = data.data["time_left"];
							$scope.shiplist = data.data["ships"]; 
							$scope.shotlist = data.data["shots"];
							if (data.data["winner"] === true || data.data["winner"] === false) {
								srvInfo.doGetPlayerInfo(function(data) { $scope.winrate = data.data["win_ratio"]; }, function(){}, token);
								$timeout.cancel($scope.timeout_promise);
								return;
							}

							$scope.shiplist = data.data["ships"]; 
							$scope.shotlist = data.data["shots"];
							$scope.turn = data.data["turn"];
						 };

						 $scope.REFRESH_INTERVAL = 1000;
						 /// Refresh function (updates the game board)
						 var refresh = function() {
						 	srvInfo.doGetBoards(get_boards_handler, function() {}, token, $scope.game);
						 };

						 $scope.on_submit_replay = function() {
							 srvInfo.requestReplay(function() {$scope.timeout_promise = $timeout(refresh, 0);}, token, $scope.game);
						 };

						 /// Leave handler
						 /// Deregisters user from game
						 $scope.onLeave = function() {
							 $timeout.cancel($scope.timeout_promise);
							 srvInfo.playerLeft(token, $scope.game);
						 };
						 
						 $scope.$on('$destroy', function(){
							 $scope.onLeave();
						 });
						 $scope.$on('$locationChangeStart', function(){
							 $scope.onLeave();
						 });
							
					 	 $scope.timeout_promise = $timeout(refresh, 0); //start calling the service
					}])
	.controller('listController',
				['$scope',
				 '$timeout',
				 '$location',
				 '$routeParams',
				 'srvInfo',
					function($scope, $timeout, $location, $routeParams, srvInfo) {
						 $scope.gamelist = [];
						 $scope.winrate = "0.0";
						 var token = $routeParams['token'];
						 var login = $routeParams['login'];

						 /// Handles game list element click
						 /// @param game - clicked game (name)
						 $scope.gameClicked = function (game) {
							 var callback = function(data) { if (data.data['valid']) { $location.path('/play').search('game',data.data['game']).search('token',token).search('login',login); }  };
							 var fallback = function() {};
							 srvInfo.doGetGame(callback, fallback, token, game, login);
						 };

						 $scope.REFRESH_INTERVAL = 1000;

						 /// Game list refresh loop
						 var refresh = function() {
							 var callback = function(data) { $scope.gamelist = data.data['games']; $scope.gamelist.push(['New Game']); };
							 var fallback = function() {};
							 srvInfo.doGetGames(callback, fallback, token);
						 	 srvInfo.doGetPlayerInfo(function(data) { $scope.winrate = data.data["win_ratio"]; }, function(){}, token);
							 timeout_promise = $timeout(refresh, $scope.REFRESH_INTERVAL); //start calling the service
						 };

						 $scope.$on('$locationChangeStart', function(){
  							 $timeout.cancel(timeout_promise);
						 });
						 $scope.$on('$destroy', function(){
  							 $timeout.cancel(timeout_promise);
						 });
							
					 	 var timeout_promise = $timeout(refresh, 0); //start calling the service
					}]);
