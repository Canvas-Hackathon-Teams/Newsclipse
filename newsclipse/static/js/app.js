var nclipse = angular.module('nclipse', ['ngRoute', 'ngAnimate']);


nclipse.controller('AppCtrl', ['$scope', '$location', '$http',
  function($scope, $location, $http) {

}]);


nclipse.controller('StoryListCtrl', ['$scope', '$location', '$http',
  function($scope, $location, $http) {
  
  $scope.stories = [];

  $http.get('/api/stories').then(function(res) {
    $scope.stories = res.data;
    console.log($scope.stories);
  });

  $scope.newStory = function() {
    var empty = {'title': '', 'text': ''};
    $http.post('/api/stories', empty).then(function(res) {
      $location.path('/stories/' + res.data._id);
    });
  };

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
    $http.post('/api/stories/' + $scope.storyId, $scope.story).then(function(res) {
      console.log('Saved the story!');
    });
  };

}]);


nclipse.directive('nclipseCard', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'story': '=',
      'card': '='
    },
    templateUrl: 'card.html',
    link: function (scope, element, attrs, model) {
      console.log('foo');
    }
  };
}]);


nclipse.directive('nclipseEvidence', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'story': '=',
      'card': '=',
      'evidence': '='
    },
    templateUrl: 'evidence.html',
    link: function (scope, element, attrs, model) {
      console.log('foo');
    }
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
