var ws = new WebSocket("ws://localhost:8899/websocket");

ws.onopen = function() {
    console.log("Socket opened");
};


ws.onclose = function() {
    console.log("Socket closed");
};


ws.onmessage = function(evt){
    console.log("Received: " + evt.data);
    var msgList = document.getElementById("msgList");
    var node = document.createElement("li");
    var text = document.createTextNode(evt.data);
    node.appendChild(text);
    msgList.appendChild(node);
};


function sendMsg(){
    var btn = document.getElementById("msg");
    console.log("Sent: "+btn.value);
    ws.send(btn.value);
    btn.value = "";
}



