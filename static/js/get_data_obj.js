console.log("=== Get Start ===") // старт скрипта
fetch('/get_json_obj', {method: 'POST'}).then(res => res.json()).then(function (data) { //фуункция получения json
    var body = document.getElementById('row-card');
    var jsn = new XMLHttpRequest();
    var ref = '/main';
    jsn.open('GET', ref, false);
    jsn.send();

    for(key in data) {

          var div = document.createElement('div');
          var div2 = document.createElement('div');
          var h5 = document.createElement('h5');
          var p = document.createElement('p');
          var col = document.createElement('div')
          p.setAttribute('class','card-text')
          h5.setAttribute('class','card-title')
          col.setAttribute('class', 'col-sm-3')
          col.setAttribute('style', 'padding-bottom: 20px')
          div2.setAttribute('class','card text-white bg-primary h-100 w-300')
          div.setAttribute('class','card-body')
          body.appendChild(col)
          p.appendChild(document.createTextNode(data[key]['address']));
          h5.appendChild(document.createTextNode(data[key]['type']));
          div.appendChild(h5)
          div.appendChild(p)
          div2.appendChild(div)
          col.appendChild(div2)
};
console.log(col)
});