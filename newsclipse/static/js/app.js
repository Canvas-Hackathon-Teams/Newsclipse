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
  var initialLoad = true,
      realText = null;

  $scope.storyId = $routeParams.id;
  $scope.story = {};
  $scope.cards = [];
  $scope.activeCards = 0;
  $scope.discardedCards = 0;
  $scope.tabs = {
    'pending': true
  };

  $scope.$on('pendingTab', function() {
    $scope.tabs.pending = true;
  });

  $http.get('/api/stories/' + $scope.storyId).then(function(res) {
    $scope.story = res.data;
    if (!$scope.story.text || !$scope.story.text.length) {
      $scope.story.text = 'Write your story here...<br><br>'
    }
  });

  $scope.$on('highlight', function(e, words) {
    realText = $scope.story.text;
    var regex = '(' + words.join('|') + ')';
    $scope.story.text = realText.replace(new RegExp(regex, 'gi'), function(t) {
      return '<span class="highlight">' + t + '</span>';
    });
  });

  $scope.$on('clearHighlight', function(e, words) {
    $scope.story.text = realText;
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
            o.evidences = c.evidences;
            o.wiki_text = c.wiki_text;
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

      scope.mouseIn = function() {
        scope.$emit('highlight', scope.card.aliases);
      };

      scope.mouseOut = function() {
        scope.$emit('clearHighlight');
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


nclipse.directive('nclipseNewCard', ['$http', 'cfpLoadingBar', function($http, cfpLoadingBar) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'story': '='
    },
    templateUrl: 'card_new.html',
    link: function (scope, element, attrs, model) {
      scope.card = {'score': 100, 'type': 'Company'};
      scope.typeOptions = ["Company", "Person", "Organization"];

      scope.selectType = function(index) {
        scope.card.type = scope.typeOptions[index];
      };

      scope.canSubmit = function() {
        return scope.card.title && scope.card.title.length > 1;
      };

      scope.saveCard = function() {
        if (!scope.canSubmit()) return;
        cfpLoadingBar.start();
        var card = angular.copy(scope.card);
        scope.card = {'score': 100, 'type': 'Company'};
        var url = '/api/stories/' + scope.story._id + '/cards';
        scope.$emit('pendingTab');
        $http.post(url, card).then(function(res) {
          scope.card = res.data;
          cfpLoadingBar.complete();
        });
      };

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
