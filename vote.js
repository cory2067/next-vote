var app = angular.module('voteApp', []);
app.controller('VoteController', function($scope, $http) {

    $scope.test = "Henlo";

    // Randomize order of voting options to ensure fairness
    for (var i=0; i<config.questions.length; i++) {
        var q = config.questions[i];
        if (q.shuffle) {
            q.options = shuffleArray(q.options);
        }
    }

    $scope.vote = config; // global var from config.js
});

app.filter('trusted', ['$sce', function ($sce) {
   return $sce.trustAsResourceUrl; // security thing to fix external URLs
}]);

// -> Fisher–Yates shuffle algorithm
var shuffleArray = function(array) {
  var m = array.length, t, i;

  // While there remain elements to shuffle
  while (m) {
    // Pick a remaining element…
    i = Math.floor(Math.random() * m--);

    // And swap it with the current element.
    t = array[m];
    array[m] = array[i];
    array[i] = t;
  }

  return array;
}
