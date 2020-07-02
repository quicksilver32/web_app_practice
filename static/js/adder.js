fetch('/adder_json', {method: 'POST'}).then(res => res.json()).then(function (data) {  //фуункция получения json
    var ul_jsn = document.getElementById('ul_json')
    var ul_jsn2 = document.getElementById('ul_json2')
    var appartment = document.getElementById('Appartment')
    var countap = 10
    var home = document.getElementById('Home')
    var jsn = new XMLHttpRequest();
    var ref = '/main';
    jsn.open('GET', ref, false);
    jsn.send();
    var ar_id = []


    var isCompany = data[Object.keys(data).length - 1]
    delete data[Object.keys(data).length - 1]
    if (isCompany == true) {
        appartment.setAttribute('style', 'display: none;')
    };

    document.getElementById('address').value = data[0]['address']
    document.getElementById('room').value = 1;

    for(key in data) {
        var l = ''
        var li_jsn = document.createElement('li');
        li_jsn.setAttribute('id', key)
        li_jsn.appendChild(document.createTextNode(data[key]['address']));
        ul_jsn.appendChild(li_jsn)
        ar_id.push(li_jsn.id)
    }

    $('#ul_json').on('click', function(e){
    var id = e.target.id
    var id_elem = document.getElementById(id)
    document.getElementById('address').value = id_elem.textContent

     $("#ul_json2").empty();
     document.getElementById('room').value = 1;

    for (let i=1; i<=data[id]['room_count']; i++){
       var li_jsn2 = document.createElement('li')
       li_jsn2.setAttribute('id', i + 'room')
       li_jsn2.appendChild(document.createTextNode(i))
       ul_jsn2.appendChild(li_jsn2)
       ar_id.push(li_jsn2.id)
    };

    });

    $('#ul_json2').on('click', function(e){
    var id = e.target.id
    var id_elem = document.getElementById(id)
    document.getElementById('room').value = id_elem.textContent
    });
});

var ul = $('.dropdown-search-box');
var input = ul.find('input');
var li = ul.find('li.result');

input.keyup(function(){
  var val = $(this).val();
  if ( val.length > 0 ) {
    li.hide();
    li.filter(':contains("'+ val +'")').show();
  } else {
    li.show();
  }
  console.log(li)
});
