/// @file services.js
/// @brief AngularJS services, AJAX communication with the server

angular.module('myAppServices', [])
    .service('srvInfo', //current information from zsm server
             function($http) {
                 this.baseURL = client_server_prefix + '/ajax/'; //the prefix defined in version.js
				 this.doLoginUser = function(callback, name, pass) {
					 return $http.get(this.baseURL + 'calcpy/loginUser', { params: { 'name': name, 'pass': pass } }).success(callback);
				 };
				 this.doUserMove = function(callback, fallback, x, y, token) {
					 return $http.get(this.baseURL + 'calcpy/userMove', { params: { 'x': x, 'y': y, 'token': token} }).then(callback, fallback);
				 };
				 this.doGetBoards = function(callback, fallback, token) {
					 return $http.get(this.baseURL + 'calcpy/getBoards', { params: { 'token': token} }).then(callback, fallback);
				 };
			 });
