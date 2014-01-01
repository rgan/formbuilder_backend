var app_module;

app_module = angular.module('formbuilderApp', ['ngCookies', 'ngResource', 'ngSanitize', 'ngRoute']);

app_module.config(function($routeProvider) {
  return $routeProvider.when('/forms/:formId/users/:userId', {
    templateUrl: "views/main.html",
    controller: "MainCtrl as mainCtrl"
  }).otherwise({
    redirectTo: "/"
  });
});

var MainCtrl;

MainCtrl = (function() {
  MainCtrl.$inject = ['$scope', '$routeParams', 'FormBuilderService'];

  function MainCtrl(scope, $routeParams, formBuilderService) {
    this.scope = scope;
    this.formBuilderService = formBuilderService;
    this.formId = $routeParams["formId"];
    this.userId = $routeParams["userId"];
    this.scope.form_data = this.formBuilderService.questionsWithAnswers(this.formId, this.userId);
  }

  MainCtrl.prototype.save = function() {
    return this.formBuilderService.save(this.formId, this.userId, this.scope.form_data, (function() {
      return alert("Saved!");
    }), (function() {
      return alert("Error saving!");
    }));
  };

  return MainCtrl;

})();

angular.module('formbuilderApp').controller('MainCtrl', MainCtrl);

angular.module('formbuilderApp').directive('choiceQuestion', function() {
  return {
    restrict: 'E',
    require: 'ngModel',
    scope: {
      question: '='
    },
    templateUrl: 'views/choice_question.html'
  };
});

angular.module('formbuilderApp').directive('essayQuestion', function() {
  return {
    restrict: 'E',
    require: 'ngModel',
    scope: {
      question: '='
    },
    templateUrl: 'views/essay_question.html'
  };
});

var FormbuilderService;

FormbuilderService = (function() {
  FormbuilderService.$inject = ['$resource', '$log'];

  function FormbuilderService(resource, log) {
    this.resource = resource;
    this.log = log;
    this.formAnswerResource = this.resource('/forms/:formId/users/:userId');
  }

  FormbuilderService.prototype.questionsWithAnswers = function(formId, userId) {
    return this.formAnswerResource.get({
      formId: formId,
      userId: userId
    });
  };

  FormbuilderService.prototype.save = function(formId, userId, form, successCallback, failureCallback) {
    return form.$save({
      formId: formId,
      userId: userId
    }, successCallback, failureCallback);
  };

  return FormbuilderService;

})();

angular.module('formbuilderApp').service('FormBuilderService', FormbuilderService);
