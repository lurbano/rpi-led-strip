$(document).ready(function(){

        var WEBSOCKET_ROUTE = "/ws";

        if(window.location.protocol == "http:"){
            //localhost
            var ws = new WebSocket("ws://" + window.location.host + WEBSOCKET_ROUTE);
        }
        else if(window.location.protocol == "https:"){
            //Dataplicity
            var ws = new WebSocket("wss://" + window.location.host + WEBSOCKET_ROUTE);
        }

        ws.onopen = function(evt) {
            // $("#ws-status").html("Connected");
            // $("#ws-status").css("background-color", "#afa");
            // $("#server_light").val("ON");
            $("#signal").html("READY");
            $("#ws-status").html("Connected");
            $("#ws-status").css("background-color", "#afa");
        };

        ws.onmessage = function(evt) {
            //console.log(evt);
            var sData = JSON.parse(evt.data);
            if (sData.sensor !== 'undefined'){
              //console.log(sData.info + "|" + )

              //WHAT TO DO WHEN WE GET A MESSAGE FROM THE SERVER
              if (sData.info == 'cleared'){
                $("#signal").html("Cleared");
              }

            };
        };

        ws.onclose = function(evt) {
            $("#ws-status").html("Disconnected");
            $("#ws-status").css("background-color", "#faa");
            $("#server_light").val("OFF");
        };

        //MESSAGES TO SEND TO THE SERVER
        $("#clearButton").click(function(){
            //var opt = $(this).val() == "OFF" ? "on" : "off";
            var msg = '{"what": "clearButton"}';
            ws.send(msg);
        });
        $("#rainbowButton").click(function(){
            var ct = $("#rainbowCount").val();
            var msg = '{"what": "rainbowButton", "opts": '+ parseInt(ct) +'}';
            ws.send(msg);
        });
        $("#blueButton").click(function(){
            //var opt = $(this).val() == "OFF" ? "on" : "off";
            var msg = '{"what": "blueButton"}';
            ws.send(msg);
        });


      });
