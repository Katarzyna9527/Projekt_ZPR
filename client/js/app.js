/// @file app.js
/// @brief main client module, AngularJS application with routing

angular.module('myApp', ['ngRoute', 'pascalprecht.translate', 'myAppControllers', 'myAppServices'] )
    .config(['$routeProvider', '$translateProvider',
             function($routeProvider, $translateProvider) {
                 $routeProvider.when('/login', {
                     templateUrl: 'views/login.html',
                 });
                 $routeProvider.when('/list', {
                     templateUrl: 'views/list.html',
                 });
                 $routeProvider.when('/play', {
                     templateUrl: 'views/play.html',
                 });
                 $routeProvider.otherwise( {
                     redirectTo: '/login'
                 });
                 $translateProvider.useStaticFilesLoader({
                      prefix: 'lang/',
                      suffix: '.json' });
                 $translateProvider.preferredLanguage('en');
             }]);

