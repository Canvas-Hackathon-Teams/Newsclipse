var nclipse = angular.module('nclipse', ['ngRoute', 'ngAnimate']);


nclipse.controller('AppCtrl', ['$scope', '$location', '$http',
  function($scope, $location, $http) {

}]);


nclipse.controller('StoryListCtrl', ['$scope', '$location', '$http',
  function($scope, $location, $http) {
  
  $scope.stories = [];

  $http.get('/api/stories').then(function(res) {
    $scope.stories = res.data;
  });

}]);


nclipse.controller('StoryCtrl', ['$scope', '$routeParams', '$location', '$http',
  function($scope, $routeParams, $location, $http) {
  
  $scope.storyId = $routeParams.id;
  $scope.story = {};
  $scope.cards = [];

  $http.get('/api/stories/' + $scope.storyId).then(function(res) {
    $scope.story = res.data;
  });

  $http.get('/api/stories/' + $scope.storyId + '/cards').then(function(res) {
    $scope.cards = res.data;
  });

  $scope.saveStory = function () {
    console.log('saving!');
  };

}]);


nclipse.config(['$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider) {

  $routeProvider.when('/', {
    templateUrl: 'story_list.html',
    controller: 'StoryListCtrl'
  });

  $routeProvider.when('/stories/:id', {
    templateUrl: 'story.html',
    controller: 'StoryCtrl'
  });

  $routeProvider.otherwise({
    redirectTo: '/'
  });

  $locationProvider.html5Mode(false);
}]);
