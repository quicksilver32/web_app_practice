console.log("=== Get Start ===") // старт скрипта
fetch('/json_request', {method: 'POST'}).then(res => res.json()).then(function (data) { //фуункция получения json
    console.log(data)
    var body = document.getElementById('row-card');


    for(key in data) {

          var div = document.createElement('div');
          var div2 = document.createElement('div');
          div2.setAttribute('id', key)
          var h5 = document.createElement('h5');
          var p = document.createElement('p');
          var col = document.createElement('div')
          var div_cont1 = document.createElement('div')
          div_cont1.setAttribute('class', 'container')
          var div_cont2 = document.createElement('div')
          div_cont2.setAttribute('class', 'container')



          var but1 = document.createElement('button')
          but1.innerHTML = 'Принять';
          var but2 = document.createElement('button')
          but2.innerHTML = 'Отклонить';
          but1.setAttribute('class', 'btn btn-outline-success btn-lg btn-block')
          //but1.setAttribute('style', 'color: #00FF7F')
          but2.setAttribute('class', 'btn btn-outline-danger btn-lg btn-block')
         //but2.setAttribute('style', 'background-color: #fcfcfc')
          div_cont1.appendChild(but1)
          div_cont2.appendChild(but2)


          p.setAttribute('class','card-text')
          h5.setAttribute('class','card-title')
          col.setAttribute('class', 'col-sm-3')
          col.setAttribute('style', 'padding-bottom: 20px')
          div2.setAttribute('class','card h-100 w-300')
          div.setAttribute('class','card-body')
          body.appendChild(col)
          p.appendChild(document.createTextNode(data[key]['room']));
          h5.appendChild(document.createTextNode(data[key]['userName']));
          div.appendChild(h5)
          div.appendChild(p)

          div.appendChild(div_cont1)
          div.appendChild(div_cont2)

          div2.appendChild(div)
          col.appendChild(div2)
};
var test = document.getElementById('0')
console.log(test.textContent)
});