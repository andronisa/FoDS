
//DOCUMENT STARTS
$(document).ready(function (){
    console.log("Document is Ready!");
    web_socket = new WebSocket("ws://localhost:8888/ws");
    web_socket.onopen = function() {
      console.log("socket opened");
    };
    web_socket.onmessage = function (evt) {
       console.log(evt.data);
    };

    $('button').click(buttonDidClick);
});


/*
    GLOBAL STRING VARIBLES
*/
var web_socket = undefined;
var MSG_TYPE_IMPORT = "import";
var MSG_TYPE_NLP = "nlp";
var MSG_TYPE_VIS = "visualise";
var Message = {
    MSG_TYPE: "",
    content: undefined
};

/**
*  This is Message Handler
*
*/
function sendMessageHandler(msgObj) {
    web_socket.send(JSON.stringify(msgObj));
}

function createMessageWithType(type, content) {
    var newMsg = Object.create(Message);
    newMsg.MSG_TYPE = type;
    newMsg.content = content;
    return newMsg;
}

/**
    Event Listeners
*/
function buttonDidClick() {
    console.log("Button: " + $(this).attr("id"));
    var buttonId = $(this).attr("id");
    var message = undefined;
    if (buttonId === 'importButton') {
        message = createMessageWithType(MSG_TYPE_IMPORT, "");
    } else if (buttonId === 'NLPButton') {
        message = createMessageWithType(MSG_TYPE_NLP, "");
    } else if (buttonId === 'visualiseButton') {
        message = createMessageWithType(MSG_TYPE_VIS, "");
    }

    sendMessageHandler(message);
}