//function refresh() {
//    location.reload()
//}
var count = 0;
fetch('/admin_obj_json', {method: 'POST'}).then(res => res.json()).then(function (data) { //фуункция получения json
    var body = document.getElementById('row-card');

    for(key in data) {
          var div = document.createElement('div');
          var div2 = document.createElement('div');
          var enter = document.createElement('div')
          enter.setAttribute('class', 'w-100')
          div2.setAttribute('id', key)
          var h5 = document.createElement('h5');
          var p = document.createElement('p');
          var col = document.createElement('div')
          var div_cont2 = document.createElement('div')
          div_cont2.setAttribute('class', 'container')
          var btn_value = data[key]['objectId']

          var but2 = document.createElement('button')
          but2.innerHTML = 'Удалить';

          but2.setAttribute('class', 'btn btn-outline-danger btn-lg btn-block')
          but2.setAttribute('value', btn_value)
//          but2.setAttribute('onclick', 'setTimeout(refresh, 100)')
          but2.setAttribute('id', key+'decline')
//          div_cont2.setAttribute('style', 'padding-bottom: 20px')
          div_cont2.appendChild(but2)


          p.setAttribute('class','card-text')
          h5.setAttribute('class','card-title')
          col.setAttribute('class', 'col-sm-3')
          col.setAttribute('style', 'padding-bottom: 20px; min-width: 300px')
          div2.setAttribute('class','card h-100')
          div.setAttribute('class','card-body')
          body.appendChild(col)
          if (data[key]['room']){
              var room = ', кв. ' + data[key]['room']
          } else {
                room = ''
          }
          p.appendChild(document.createTextNode(data[key]['address'] + room));
          room = ''
          h5.appendChild(document.createTextNode(data[key]['userName']));
          div.appendChild(h5)
          div.appendChild(p)

          div2.appendChild(div)
          div2.appendChild(div_cont2)
          col.appendChild(div2)

          if (count == 3){
            count = 0;
            body.appendChild(enter)
          }
          else{
            count++
          }
};
$('button').on('click', function(e){
    var id = e.target.id
    var elem = document.getElementById(id)
    var elem1 = elem.parentNode
    var elem2 = elem1.parentNode
    var elem3 = elem2.parentNode
    elem3.style.display = 'none'
    fetch('/obj_change?data='+ elem.value);
    elem3.style.display = 'none'
    });
});
