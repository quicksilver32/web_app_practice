console.log("=== Get Start ===") // старт скрипта
fetch('/get_json_obj', {method: 'POST'}).then(res => res.json()).then(function (data) { //фуункция получения json
    console.log(data)
    var body = document.getElementById('row-card');
    var jsn = new XMLHttpRequest();
    var ref = '/main';
    jsn.open('GET', ref, false);
    jsn.send();

    //var h1 = document.createElement('h1');
    //h1.appendChild(document.createTextNode(data[0]))
    for(key in data) {

          var div = document.createElement('div');
          var div2 = document.createElement('div');
          var h5 = document.createElement('h5');
          var p = document.createElement('p');
          p.setAttribute('class','card-text')
          h5.setAttribute('class','card-title')
          div2.setAttribute('class','card')
          div.setAttribute('class','card-body')
          p.appendChild(document.createTextNode(data[key]['address']));
          h5.appendChild(document.createTextNode(data[key]['type']));
          div.appendChild(h5)
          div.appendChild(p)
          div2.appendChild(div)
          body.appendChild(div2)
};

});