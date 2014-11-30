var nclipse = angular.module('nclipse', ['ngRoute', 'ngAnimate', 'ui.bootstrap']);


nclipse.controller('AppCtrl', ['$scope', '$location', '$http',
  function($scope, $location, $http) {

  $scope.newStory = function() {
    var empty = {'title': '', 'text': ''};
    $http.post('/api/stories', empty).then(function(res) {
      $location.path('/stories/' + res.data._id);
    });
  };

}]);


nclipse.controller('StoryListCtrl', ['$scope', '$location', '$http',
  function($scope, $location, $http) {
  
  $scope.stories = [];

  $http.get('/api/stories').then(function(res) {
    $scope.stories = res.data;
  });

}]);


nclipse.controller('StoryCtrl', ['$scope', '$routeParams', '$location', '$interval', '$http',
  function($scope, $routeParams, $location, $interval, $http) {
  
  $scope.storyId = $routeParams.id;
  $scope.story = {};
  $scope.cards = [];

  $http.get('/api/stories/' + $scope.storyId).then(function(res) {
    $scope.story = res.data;
  });

  var updateCards = function() {
    $http.get('/api/stories/' + $scope.storyId + '/cards').then(function(res) {
      var newCards = [];
      angular.forEach(res.data, function(c) {
        var exists = false;
        angular.forEach($scope.cards, function(o) {
          if (o['_id'] == c['_id']) {
            exists = true; 
          }
        });
        if (!exists) newCards.push(c);
      });
      newCards = newCards.concat($scope.cards);
      newCards.sort(function(a, b) {
        if (a.offset == b.offset) {
          return a.updated_at.localeCompare(b.updated_at);
        }
        return a.offset - b.offset;
      });
      $scope.cards = newCards;
    });
  };

  $interval(updateCards, 2000);
  
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
      var url = '/api/stories/' + scope.story._id + '/cards/' + scope.card._id;
      scope.mode = 'view';

      scope.toggleMode = function() {
        if (scope.editMode()) {
          $http.post(url, scope.card).then(function(res) {
            scope.card = res.data;
          });
        }
        scope.mode = scope.mode == 'view' ? 'edit' : 'view';
      };

      scope.editMode = function() {
        return scope.mode == 'edit';
      };

      scope.viewMode = function() {
        return scope.mode == 'view';
      };

      scope.hasEvidence = function() {
        return scope.card.evidences.length > 0;
      };

      scope.hasAliases = function() {
        return scope.card.aliases.length > 1;
      };
    }
  };
}]);


nclipse.directive('nclipseNewCard', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'story': '='
    },
    templateUrl: 'card_new.html',
    link: function (scope, element, attrs, model) {
      scope.card = {'score': 100};

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
