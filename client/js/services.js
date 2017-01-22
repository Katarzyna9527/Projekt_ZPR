/// @file services.js
/// @brief AngularJS services, AJAX communication with the server

angular.module('myAppServices', [])
    .service('srvInfo', //current information from zsm server
             function($http) {
                 this.baseURL = client_server_prefix + '/ajax/'; //the prefix defined in version.js
				 this.doLoginUser = function(callback, fallback, name, pass) {
					 return $http.get(this.baseURL + 'calcpy/loginUser', { params: { 'name': name, 'pass': pass } }).then(callback, fallback);
				 };
				 this.doRegisterUser = function(callback, fallback, name, pass) {
					 return $http.get(this.baseURL + 'calcpy/registerUser', { params: { 'name': name, 'pass': pass } }).then(callback, fallback);
				 };
				 this.doUserMove = function(callback, fallback, x, y, token, game) {
					 return $http.get(this.baseURL + 'calcpy/userMove', { params: { 'x': x, 'y': y, 'token': token, 'game': game } }).then(callback, fallback);
				 };
				 this.doGetBoards = function(callback, fallback, token, game) {
					 return $http.get(this.baseURL + 'calcpy/getBoards', { params: { 'token': token, 'game': game } }).then(callback, fallback);
				 };
				 this.doGetGames = function(callback, fallback, token) {
					 return $http.get(this.baseURL + 'calcpy/getGames', { params: { 'token': token } }).then(callback, fallback);
				 };
				 this.doGetGame = function(callback, fallback, token, game) {
					 return $http.get(this.baseURL + 'calcpy/getGame', { params: { 'token': token, 'game': game } }).then(callback, fallback);
				 };
				 this.doGetPlayerInfo = function(callback, fallback, token) {
					 return $http.get(this.baseURL + 'calcpy/getPlayerInfo', { params: { 'token': token } }).then(callback, fallback);
				 };
			 });
