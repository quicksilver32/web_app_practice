console.log("=== Get Start ===") // старт скрипта
fetch('/get_json_obj', {method: 'POST'}).then(res => res.json()).then(function (data) { //фуункция получения json
    console.log(data)
    var body = document.getElementById('body');
    var jsn = new XMLHttpRequest();
    var ref = '/main';
    jsn.open('GET', ref, false);
    jsn.send();

    //var h1 = document.createElement('h1');
    //h1.appendChild(document.createTextNode(data[0]))
    body.appendChild(document.createTextNode(data[0]['address'] + "  "));
    body.appendChild(document.createTextNode(data[0]['type'] + "........."));
    body.appendChild(document.createTextNode(data[1]['address'] + "  "));
    body.appendChild(document.createTextNode(data[1]['type'] + "  "));
});