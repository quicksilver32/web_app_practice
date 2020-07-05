fetch('/admin_json_dashboard', {method: 'POST'}).then(res => res.json()).then(function (data) {  //фуункция получения json
    console.log(data)
    var sel0 = document.getElementById('dropdown0')
    var sel1 = document.getElementById('dropdown1')
    var sel2 = document.getElementById('dropdown2')
    var sel3 = document.getElementById('dropdown3')
    var sel4 = document.getElementById('dropdown4')
//    var opt0 = document.createElement('option')
//    var opt1 = document.createElement('option')
//    var opt2 = document.createElement('option')
//    var opt3 = document.createElement('option')
//    var opt4 = document.createElement('option')
    for (key in data['regions']) {
        var opt0 = document.createElement('option')
        opt0.innerHTML = data['regions'][key]['name']
        sel0.appendChild(opt0)
    }
    for (key in data['cities']) {
        var opt1 = document.createElement('option')
        opt1.innerHTML = data['cities'][key]['name']
        sel1.appendChild(opt1)
    }
    for (key in data['buildings']) {
        var opt2 = document.createElement('option')
        var opt3 = document.createElement('option')
        opt3.setAttribute('id', key)
        opt3.setAttribute('class', 'room')
        opt2.innerHTML = data['buildings'][key]['address']
        sel2.appendChild(opt2)
        opt3.innerHTML = data['buildings'][key]['address']
        sel3.appendChild(opt3)
    }
    for (let i = 1; i <= Number(data['buildings'][0]['room_count_live']); i++) {
        var opt4 = document.createElement('option')
        opt4.innerHTML = i
        sel4.appendChild(opt4)
    }
    console.log(sel3)
//    $('#0').on('click', function(e){
//    var id = e.target.id
//    console.log(id)
//    //var id_elem = document.getElementById(id)
//    var room = data['buildings'][id]['room_count_live']
//    //console.log(id)
//    for (let i = 1; i <= room; i++) {
//        var opt4 = document.createElement('option')
//        opt4.innerHTML = i
//        sel4.appendChild(opt4)
//    }
//    });
});
