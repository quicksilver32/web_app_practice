var ul = $('.dropdown-search-box');
var input = ul.find('input');
var li = ul.find('li.result');

input.keyup(function(){
  var val = $(this).val();
  if ( val.length > 1 ) {
    li.hide();
    li.filter(':contains("'+ val +'")').show();
  } else {
    li.show();
  }
});

fetch('/adder_json', {method: 'POST'}).then(res => res.json()).then(function (data) {  //фуункция получения json
    var ul_jsn = document.getElementById('ul_json')
    var jsn = new XMLHttpRequest();
    var ref = '/main';
    jsn.open('GET', ref, false);
    jsn.send();
    var ar_id = []
    for(key in data) {
        var l = ''
        var li_jsn = document.createElement('li');
        li_jsn.setAttribute('id', key)
        li_jsn.appendChild(document.createTextNode(data[key]['address']));
        ul_jsn.appendChild(li_jsn)
        ar_id.push(li_jsn.id)
     }
     $('li').on('click', function(e){
     var id = e.target.id
     var id_elem = document.getElementById(id)
     var lb = document.getElementById('label')
     var label = document.createElement('label');
     lb.innerHTML = id_elem.textContent
});
});

