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
	.controller('versionController', //versions of system modules
				['$scope',
				 'srvInfo',
				 function($scope, srvInfo) {
					 srvInfo.getVersion(
					 	 function(data) {
					 		 $scope.server_ver = data;
					 	 });
					 srvInfo.getCppNumber(
						 function(data) {
							 $scope.cpp_get = data;
						 });
					 $scope.client_ver = client_ver_major.toString() + '.' + client_ver_minor.toString() + '.' + client_ver_compilation.toString(); //from version.js file
				 }])
	.controller('commandController', //cpp commands
				['$scope',
				 'srvCommands',
				 function($scope, srvCommands) {
					 $scope.getCppCommandsNo = function() {
						 srvCommands.getCppCommands(
							 function(data) {
								 $scope.cpp_commands_no = Object.keys(data).length;
							 });
					 };
					 $scope.clickNewCommand = function() {
						 srvCommands.startCommand(
							 function(data) {
								 $scope.getCppCommandsNo();
							 })
					 };
					 $scope.getCppCommandsNo();
				 }])
	.controller('currentController', //current server params
				['$scope',
				 '$timeout',
				 'srvInfo',
				 'srvCommands',
				 function($scope, $timeout, srvInfo, srvCommands) {
					 var REFRESH_INTERVAL = 1000; //ms

					 var call = function() { //function called periodically
						 $scope.getCppCommands = function() {
							 srvCommands.getCppCommands(
								 function(data) {
									 $scope.cpp_commands = data;
								 });
						 };

						 srvInfo.getCurrent(
					 		 function(data) {
					 			 $scope.current = data;
								 $scope.getCppCommands();
								 $timeout(call, REFRESH_INTERVAL);
					 		 });
					 };
					 $timeout(call, 0); //start calling the service
				 }])
	.controller('loginController',
				['$scope',
				 'srvInfo',
				 function($scope, srvInfo) {
					 $scope.on_submit_login = function() {
					 	 var callback = function (data) { console.log("Login OK: ",data); };
						 srvInfo.doLoginUser(callback, $scope.account_name, $scope.account_password);
					 };
				 }])
	.controller('gameController',
				['$scope',
				 'srvInfo',
					function($scope, srvInfo) {
						 $scope.shiplist = [[],[],[],[],[],[],[],[]]
						 function Ship(xpos, ypos, shiplist = $scope.shiplist) {
							 this.xpos = xpos;
							 this.ypos = ypos;
							 this.up = true;
							 shiplist[xpos][ypos] = "up";
						 }

						 $scope.ships = [Ship(0, 0), Ship(0, 1), Ship(0, 2), Ship(3, 2), Ship(3, 3)];
						 $scope.shotlist = [[],[],[],[],[],[],[],[]];

						 console.log($scope.shiplist);
						 $scope.clicked_gamecell = function (xpos, ypos) {
							 $scope.shotlist[xpos][ypos]="down";
						 };
					}]);

