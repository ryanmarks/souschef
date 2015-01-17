var App = angular.module('SousChef', []);

App.controller('ContentController', ['$scope','$http',function($scope, $http){
    $scope.submitSearch = function (){
        $http.post('/recipe/get/all',{search:$scope.searchValue}).success(function(data){
            $scope.searchOptions = data;
        })
    }
    
    $scope.activateSpeechRecog = function(){
        
          var recognition = new webkitSpeechRecognition();
          recognition.continuous = true;
          recognition.interimResults = false;
          recognition.onstart = function() {console.log('Speech Recognition Commencing')}
          recognition.onresult = function(event) {
              for (var i = event.resultIndex; i < event.results.length; ++i) {
                  if (event.results[i].isFinal) {
                    $.ajax({
                      url: 'https://api.wit.ai/message',
                      data: {
                        'q': event.results[i][0].transcript,
                        'access_token' : 'SMRYKLMQBVUVUFDAPTPTXLY6H2ZM4DQU'
                      },
                      dataType: 'jsonp',
                      method: 'GET',
                      success: function(response) {
                          console.log("success!", response);
                          if(response.outcomes[0].confidence>0.6){
                             $.ajax({
                              url: '/functions',
                              data: {
                                'intent':response.outcomes[0].intent,
                                'entities':response.outcomes[0].entities
                              },
                              dataType: 'jsonp',
                              method: 'GET',
                              success: function(response) {
                                  console.log("Sent intent back to server and nothing failed!");
                                  
                              }
                            });
                          }
                      }
                    });
                  }
              }
          }                                     
        

            recognition.lang = 'en-US';
            recognition.start();
    }
}])