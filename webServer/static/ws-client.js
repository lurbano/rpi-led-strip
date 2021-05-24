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
            //console.log(sData);
            if (sData.sensor !== 'undefined'){
              //console.log(sData.info + "|" + )

              //WHAT TO DO WHEN WE GET A MESSAGE FROM THE SERVER

              // LED STRIP (1/2)

              if (sData.info == 'cleared'){
                $("#signal").html("Cleared");
              }

              //LED STRIP


              // TIMER (1/2)

              if (sData.info == 'timer'){
                m = sData.m.toString();
                s = sData.s.toString().padStart(2,"0");
                $("#timeLeft").html(m + ":" + s);
              }

              // TIMER (END)


            };
        };

        ws.onclose = function(evt) {
            $("#ws-status").html("Disconnected");
            $("#ws-status").css("background-color", "#faa");
            $("#server_light").val("OFF");
        };

        //MESSAGES TO SEND TO THE SERVER

        // LED STRIP (2/2)

        $("#nPix").change(function(){
            let nPix = this.value;
            let check = confirm("Change Number of Pixels to: " + nPix);
            if (check){
              let msg = {"what": "nPix", "n": nPix};
              ws.send(JSON.stringify(msg));

            }
        });

        $("#clearButton").click(function(){
            var msg = '{"what": "clearButton"}';
            ws.send(msg);
        });
        $("#rainbowButton").click(function(){
            var ct = $("#rainbowCount").val();
            var s = $("#rainbowSpeed").val();
            let msg = {
              "what": "rainbowButton",
              "ct": parseInt(ct),
              "speed": s
            }
            ws.send(JSON.stringify(msg));
        });
        $("#rainbowForever").click(function(){
            let msg = {
              "what": "rainbowForever",
              "speed": $("#rainbowSpeed").val()
            }
            ws.send(JSON.stringify(msg));
        });

        $("#setColor").change(function(){
            let msg = {
              "what": "setColor",
              "color": this.value
            }
            ws.send(JSON.stringify(msg));
        });
        $("#setBrightness").change(function(){
            let msg = {
              "what": "setBrightness",
              "brightness": this.value
            }
            ws.send(JSON.stringify(msg));
        });
        $("#interruptButton").click(function(){
            var msg = '{"what": "interruptButton"}';
            ws.send(msg);
        });
        $("#blueButton").click(function(){
            var msg = '{"what": "blueButton"}';
            ws.send(msg);
        });

        $("#sinX").click(function(){
            var f = $("#sinXFreq").val();
            var p = $("#sinXPhase").val();
            var c = $("#sinXColor").val();
            let msg = {
              "what": "sinX",
              "freq": f,
              "phase": p,
              "color": c
            }
            ws.send(JSON.stringify(msg));
        });

        sinXPhase_down = false;
        $("#sinXPhaseLive").mousedown(function(){
          sinXPhase_down = true;
        });
        $("#sinXPhaseLive").mouseup(function(){
          sinXPhase_down = false;
        });
        $("#sinXPhaseLive").mousemove(function(){
          if (sinXPhase_down){
            var f = $("#sinXFreqLive").val();
            var p = $(this).val();
            var c = $("#sinXColorLive").val();
              let msg = {
                "what": "sinXPhaseLive",
                "freq": f,
                "phase": p,
                "color": c
              }
              ws.send(JSON.stringify(msg));
            }
        });
        $("#sinXColorLive").change(function(){
          var f = $("#sinXFreqLive").val();
          var p = $("#sinXPhaseLive").val();
          var c = $(this).val();
          let msg = {
            "what": "sinX",
            "freq": f,
            "phase": p,
            "color": c
          }
          ws.send(JSON.stringify(msg));
        })

        // LED STRIP (END)


        // TIMER (2/2)

        $("#timer").click(function(){
            let m = $("#timerMin").val();
            let s = $("#timerSec").val();
            let msg = '{"what": "timer", "minutes":'+ m + ', "seconds": '+ s + '}';
            ws.send(msg);
        });

        // TIMER (END)


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


        $(".flagButton").click(function(){

          let id = this.id;
          let prefix = id.split("_")[0];
          let ctrlDiv = $("#"+prefix+"_CONTROLS");
          console.log(this.id);
          ctrlDiv.toggle();
          //now toggle visibility
        });

      });
