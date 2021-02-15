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
            var s = $("#rainbowSpeed").val();
            var msg = '{"what": "rainbowButton", "ct": '+ parseInt(ct) +', "speed":'+ s +'}';
            ws.send(msg);
        });
        $("#rainbowForever").click(function(){
            var s = $("#rainbowSpeed").val();
            var msg = '{"what": "rainbowForever", "speed":'+ s +'}';
            ws.send(msg);
        });
        $("#timer").click(function(){
            let m = $("#timerMin").val();
            let s = $("#timerSec").val();
            let msg = '{"what": "timer", "minutes":'+ m + ', "seconds": '+ s + '}';
            ws.send(msg);
        });
        $("#restart").click(function(){
          let check = confirm("Restart Server?");
          if (check){
            var msg = '{"what": "restart"}';
            ws.send(msg);
          }
        });
        $("#reboot").click(function(){
            let check = confirm("Reboot Pi?");
            if (check){
              var msg = '{"what": "reboot"}';
              ws.send(msg);
            }
        });
        $("#setColor").change(function(){
            var col = this.value;
            var msg = '{"what": "setColor", "color": "'+ col +'"}';
            ws.send(msg);
        });
        $("#setBrightness").change(function(){
            var bright = this.value;
            var msg = '{"what": "setBrightness", "brightness": "'+ bright +'"}';
            ws.send(msg);
        });
        $("#interruptButton").click(function(){
            var msg = '{"what": "interruptButton"}';
            ws.send(msg);
        });
        $("#blueButton").click(function(){
            var msg = '{"what": "blueButton"}';
            ws.send(msg);
        });



      });
