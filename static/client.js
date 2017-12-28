function sendGet(link){
    var url = 'localhost:8899' + link;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function printResponse(link){
    var response = sendGet(link);
    console.log(response);
}
