var nclipse = angular.module('nclipse', ['ngRoute', 'ngAnimate', 'ui.bootstrap', 'angular-loading-bar', 'contenteditable', 'truncate']);

nclipse.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
  cfpLoadingBarProvider.includeSpinner = false;
  cfpLoadingBarProvider.latencyThreshold = 500;
  //cfpLoadingBarProvider.parentSelector = 'section';
}]);

nclipse.controller('AppCtrl', ['$scope', '$location', '$http', 'cfpLoadingBar',
  function($scope, $location, $http, cfpLoadingBar) {

  $scope.newStory = function() {
    cfpLoadingBar.start();
    var empty = {'title': '', 'text': ''};
    $http.post('/api/stories', empty).then(function(res) {
      $location.path('/stories/' + res.data._id);
      cfpLoadingBar.complete();
    });
  };

}]);


nclipse.controller('StoryListCtrl', ['$scope', '$location', '$http', 'cfpLoadingBar',
  function($scope, $location, $http, cfpLoadingBar) {
  
  $scope.stories = [];

  cfpLoadingBar.start();
  $http.get('/api/stories').then(function(res) {
    $scope.stories = res.data;
    cfpLoadingBar.complete();
  });

}]);


nclipse.controller('StoryCtrl', ['$scope', '$routeParams', '$location', '$interval', '$http', 'cfpLoadingBar',
  function($scope, $routeParams, $location, $interval, $http, cfpLoadingBar) {
  var initialLoad = true;

  $scope.storyId = $routeParams.id;
  $scope.story = {};
  $scope.cards = [];
  $scope.activeCards = 0;
  $scope.discardedCards = 0;

  $http.get('/api/stories/' + $scope.storyId).then(function(res) {
    $scope.story = res.data;
  });

  var updateCards = function() {
    if (initialLoad) {
      cfpLoadingBar.start();
    }
    $http.get('/api/stories/' + $scope.storyId + '/cards', {ignoreLoadingBar: true}).then(function(res) {
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
      $scope.discardedCards = 0;
      $scope.activeCards = 0;

      angular.forEach(newCards, function(c) {
        c.discarded = c.status == 'discarded';
        if (c.discarded) {
          $scope.discardedCards++;
        } else {
          $scope.activeCards++;
        }
      });

      $scope.cards = newCards;
      if (initialLoad) {
        initialLoad = false;
        cfpLoadingBar.complete();
      }
    });
  };

  $interval(updateCards, 2000);
  
  $scope.saveStory = function () {
    cfpLoadingBar.start();
    $http.post('/api/stories/' + $scope.storyId, $scope.story).then(function(res) {
      console.log('Saved the story!');
      cfpLoadingBar.complete();
    });
  };

}]);

nclipse.directive('nclipseCard', ['$http', 'cfpLoadingBar', function($http, cfpLoadingBar) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'story': '=',
      'card': '='
    },
    templateUrl: 'card.html',
    link: function (scope, element, attrs, model) {
      scope.mode = 'view';
      scope.expanded = false;

      var saveCard = function() {
        cfpLoadingBar.start();
        var url = '/api/stories/' + scope.story._id + '/cards/' + scope.card._id;
        scope.card.discarded = scope.card.status == 'discarded';
        $http.post(url, scope.card).then(function(res) {
          scope.card = res.data;
          scope.card.discarded = scope.card.status == 'discarded';
          cfpLoadingBar.complete();
        });
      };

      scope.toggleMode = function() {
        if (scope.editMode()) {
          saveCard();
        }
        scope.mode = scope.mode == 'view' ? 'edit' : 'view';
      };

      scope.toggleDiscarded = function() {
        if (scope.card.status == 'discarded') {
          scope.card.status = 'approved';
        } else {
          scope.card.status = 'discarded';
        }
        saveCard();
      };

      scope.expandCard = function() {
        scope.expanded = !scope.expanded;
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

      scope.hasWiki = function() {
        if(scope.card.wiki_text != undefined){
          return scope.card.wiki_text.length > 0;
        }else{
          return false;
        }
      };

      scope.hasCustom = function() {
        return scope.card.text.length > 0;
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
