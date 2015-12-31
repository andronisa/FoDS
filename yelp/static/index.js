
//DOCUMENT STARTS
$(document).ready(function (){
    console.log("Document is Ready!");
    var ws = new WebSocket("ws://localhost:8888/ws");
    ws.onopen = function() {
       ws.send("Hello, world");
    };
    ws.onmessage = function (evt) {
       alert(evt.data);
    };
});


/*
    GLOBAL STRING VARIBLES
*/
