console.log("=== Get Start ===") // старт скрипта
function refresh() {
    location.reload()
}
fetch('/json_request', {method: 'POST'}).then(res => res.json()).then(function (data) { //фуункция получения json
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
          if (data[key]['room'] == null){
              var btn_room = ''
          } else {
            btn_room = data[key]['room']
          };
          var btn_value = data[key]['userId'] + '_' + data[key]['buildingId'] + "_" + btn_room + "_" + data[key]['requestId']

          var but1 = document.createElement('button')
          but1.innerHTML = 'Принять';
          var but2 = document.createElement('button')
          but2.innerHTML = 'Отклонить';
          but1.setAttribute('class', 'btn btn-outline-success btn-lg btn-block')
          but1.setAttribute('value', btn_value+'_accept')
          but1.setAttribute('onclick', 'setTimeout(refresh, 100)')
          but1.setAttribute('id', key+'accept')
          but2.setAttribute('class', 'btn btn-outline-danger btn-lg btn-block')
          but2.setAttribute('value', btn_value+'_decline')
          but2.setAttribute('onclick', 'setTimeout(refresh, 100)')
          but2.setAttribute('id', key+'decline')
          div_cont1.appendChild(but1)
          div_cont2.appendChild(but2)


          p.setAttribute('class','card-text')
          h5.setAttribute('class','card-title')
          col.setAttribute('class', 'col-sm-3')
          col.setAttribute('style', 'padding-bottom: 20px')
          div2.setAttribute('class','card h-100 w-300')
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

          div.appendChild(div_cont1)
          div.appendChild(div_cont2)

          div2.appendChild(div)
          col.appendChild(div2)
};
$('button').on('click', function(e){
    var id = e.target.id
    var id_elem = document.getElementById(id)
    fetch('/req_change?data='+id_elem.value);
    });
});
