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
				 '$rootScope',
				 '$location',
				 'srvInfo',
				 function($scope, $rootScope, $location, srvInfo) {
					 $scope.login_failed = false;
					 $scope.register_failed = false;
					 $scope.on_submit_login = function() {
					 	 var callback = function (data) { if (data.data["session-token"]) { $rootScope.token = data.data["session-token"]; $location.path('/play'); } else { $scope.login_failed = true; }};
						 var fallback = function () { console.log("Login failed"); };
						 srvInfo.doLoginUser(callback, fallback, $scope.account_name, $scope.account_password);
					 };
					 $scope.on_submit_register = function() {
					 	 var callback = function (data) { if (data.data["session-token"]) { $rootScope.token = data.data["session-token"]; $location.path('/play'); } else { $scope.login_failed = true; }};
						 var fallback = function () { $scope.register_failed = true; };
						 srvInfo.doRegisterUser(callback, fallback, $scope.account_name, $scope.account_password);
					 };

				 }])
	.controller('gameController',
				['$scope',
				 '$rootScope',
				 '$timeout',
				 'srvInfo',
					function($scope, $rootScope, $timeout, srvInfo) {
						 $scope.shiplist = [[],[],[],[],[],[],[],[],[],[]];
						 $scope.shotlist = [[],[],[],[],[],[],[],[],[],[]];

						 console.log($rootScope.token);
					
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
								 $scope.REFRESH_INTERVAL = 1000;
								 }, function() {}, xpos, ypos, $rootScope.token );
						 };

						 $scope.REFRESH_INTERVAL = 3000;
						 var refresh = function() {
						 	srvInfo.doGetBoards(function(data) {
								console.log(data);
								$scope.shiplist = data.data["ships"]; 
								$scope.shotlist = data.data["shots"];
								$scope.turn = data.data["turn"];
								if ($scope.turn) $scope.REFRESH_INTERVAL = 5000;
								else $scope.REFRESH_INTERVAL = 1000;
								}, function() {}, $rootScope.token);
					 	 		
								$timeout(refresh, $scope.REFRESH_INTERVAL); //start calling the service
							};
						 
							
					 	 $timeout(refresh, 0); //start calling the service
					}])
	.controller('listController',
				['$scope',
				 '$rootScope',
				 '$timeout',
				 'srvInfo',
					function($scope, $rootScope, $timeout, srvInfo) {
						 $scope.gamelist = [];

						 $scope.clicked_game = function (xpos, ypos) {
						 };

						 $scope.REFRESH_INTERVAL = 1000;
						 var refresh = function() {
							$timeout(refresh, $scope.REFRESH_INTERVAL); //start calling the service
						 };
							
					 	 $timeout(refresh, 0); //start calling the service
					}]);
