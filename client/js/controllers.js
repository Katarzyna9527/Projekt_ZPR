/// @file controllers.js
/// @brief AngularJS controllers

angular.module('myAppControllers', [])
	.controller('settingsController', //client static settings
				['$scope',
				 '$translate',
				 function($scope, $translate) {
					 $scope.langs = ['en', 'pl'];
					 $scope.changeLanguage = function (lang) {
						 $translate.use(lang);
					 };
				 }])
	.controller('loginController',
				['$scope',
				 '$location',
				 'srvInfo',
				 function($scope, $location, srvInfo) {
					 var callback = function (data) { if (data.data["session-token"]) { token = data.data["session-token"]; $location.path('/list').search('token',token); } else { $scope.login_failed = true; }};
					 var fallback = function () { console.log("Login failed"); };

					 $scope.login_failed = false;
					 var token = -1;

					 $scope.on_submit_login = function() {
						 srvInfo.doLoginUser(callback, fallback, $scope.account_name, $scope.account_password);
					 };
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
						 var game = $routeParams['game'];

						 $scope.turn = true;
						 $scope.clicked_gamecell = function (xpos, ypos) {
							 if ($scope.shotlist[xpos][ypos]) { console.log("Cannot shoot there"); return; }
							 if ($scope.turn == false) { console.log("Not your turn"); return; }
							 srvInfo.doUserMove(function(data) { 
								 if (data.data["valid"] != 1) { 
									 return; }
								 if (data.data["hit"] == 1) { 
									 $scope.shotlist[xpos][ypos]="hit"; }
								 else {
									 $scope.shotlist[xpos][ypos]="miss"; }

								 $scope.turn = false;
								 $scope.REFRESH_INTERVAL = 2000;
								 }, function() {}, xpos, ypos, token, game);
						 };

						 $scope.REFRESH_INTERVAL = 5000;
						 var refresh = function() {
						 	srvInfo.doGetBoards(function(data) {
								console.log(data);
								$scope.shiplist = data.data["ships"]; 
								$scope.shotlist = data.data["shots"];
								$scope.turn = data.data["turn"];
								$scope.won = data.data["winner"];
								if (data.data["winner"] === true || data.data["winner"] === false) {
									srvInfo.doGetPlayerInfo(function(data) { $scope.winrate = data.data["win_ratio"]; }, function(){}, token);
  							 		$timeout.cancel(timeout_promise);
									return;
								}

								if ($scope.turn) $scope.REFRESH_INTERVAL = 5000;
								else $scope.REFRESH_INTERVAL = 1000;
								}, function() {}, token, game);
					 	 		
								$timeout(refresh, $scope.REFRESH_INTERVAL); //start calling the service
						 };
						 
						 $scope.$on('$destroy', function(){
  							 $timeout.cancel(timeout_promise);
						 });
						 $scope.$on('$locationChangeStart', function(){
  							 $timeout.cancel(timeout_promise);
						 });
							
					 	 var timeout_promise = $timeout(refresh, 0); //start calling the service
					}])
	.controller('listController',
				['$scope',
				 '$timeout',
				 '$location',
				 '$routeParams',
				 'srvInfo',
					function($scope, $timeout, $location, $routeParams, srvInfo) {
						 $scope.gamelist = [];
						 var token = $routeParams['token'];

						 $scope.gameClicked = function (game) {
							 var callback = function(data) { if (data.data['valid']) { $location.path('/play').search('game',data.data['game']).search('token',token); }  };
							 var fallback = function() {};
							 srvInfo.doGetGame(callback, fallback, token, game);
						 };

						 $scope.REFRESH_INTERVAL = 1000;
						 var refresh = function() {
							 var callback = function(data) { $scope.gamelist = data.data['games']; $scope.gamelist.push('New Game'); };
							 var fallback = function() {};
							 srvInfo.doGetGames(callback, fallback, token);
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
