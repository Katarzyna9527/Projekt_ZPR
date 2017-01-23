/// @file services.js
/// @brief AngularJS services, AJAX communication with the server

angular.module('myAppServices', [])
    .service('srvInfo', //current information from zsm server
             function($http) {
                 this.baseURL = client_server_prefix + '/ajax/'; //the prefix defined in version.js
				 /// Request login
				 /// @param callback - function to call on success
				 /// @param fallback - function to call on failure
				 /// @param name - user input login
				 /// @param pass - user input password (unhashed - only via https)
				 this.doLoginUser = function(callback, fallback, name, pass) {
					 return $http.get(this.baseURL + 'calcpy/loginUser', { params: { 'name': name, 'pass': pass } }).then(callback, fallback);
				 };
				 /// Request user registration
				 /// @param callback - function to call on success
				 /// @param fallback - function to call on failure
				 /// @param name - user input login
				 /// @param pass - user input password (unhashed - only via https)
				 this.doRegisterUser = function(callback, fallback, name, pass) {
					 return $http.get(this.baseURL + 'calcpy/registerUser', { params: { 'name': name, 'pass': pass } }).then(callback, fallback);
				 };
				 /// Request move
				 /// @param callback - function to call on success
				 /// @param fallback - function to call on failure
				 /// @param x - the x coordinate
				 /// @param y - the y coordinate
				 /// @param token - the user's token
				 /// @param game - the game name
				 this.doUserMove = function(callback, fallback, x, y, token, game) {
					 return $http.get(this.baseURL + 'calcpy/userMove', { params: { 'x': x, 'y': y, 'token': token, 'game': game } }).then(callback, fallback);
				 };
				 /// Request game boards
				 /// @param callback - function to call on success
				 /// @param fallback - function to call on failure
				 /// @param token - the user's token
				 /// @param game - the game name
				 this.doGetBoards = function(callback, fallback, token, game) {
					 return $http.get(this.baseURL + 'calcpy/getBoards', { params: { 'token': token, 'game': game } }).then(callback, fallback);
				 };
				 /// Request games list
				 /// @param callback - function to call on success
				 /// @param fallback - function to call on failure
				 /// @param token - the user's token
				 this.doGetGames = function(callback, fallback, token) {
					 return $http.get(this.baseURL + 'calcpy/getGames', { params: { 'token': token } }).then(callback, fallback);
				 };
				 /// Request to join a game
				 /// @param callback - function to call on success
				 /// @param fallback - function to call on failure
				 /// @param token - the user's token
				 /// @param game - the game name
				 /// @param login - the user's login
				 this.doGetGame = function(callback, fallback, token, game, login) {
					 return $http.get(this.baseURL + 'calcpy/getGame', { params: { 'token': token, 'game': game, 'login': login } }).then(callback, fallback);
				 };
				 /// Request 
				 /// @param callback - function to call on success
				 /// @param fallback - function to call on failure
				 /// @param token - the user's token
				 this.doGetPlayerInfo = function(callback, fallback, token) {
					 return $http.get(this.baseURL + 'calcpy/getPlayerInfo', { params: { 'token': token } }).then(callback, fallback);
				 };
				 /// Request games list
				 /// @param callback - function to call on success
				 /// @param fallback - function to call on failure
				 /// @param token - the user's token
				 this.playerLeft = function(token, game) {
					 return $http.get(this.baseURL + 'calcpy/onPlayerLeave', { params: { 'token': token, 'game': game } });
				 };

				 /// Request replay
				 this.requestReplay = function(callback, token, game) {
					 return $http.get(this.baseURL + 'calcpy/onReplayRequest', { params: { 'token': token, 'game': game } }).success(callback);
				 };
			 });
