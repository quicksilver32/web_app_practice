fetch('/json_dashboard', {method: 'POST'}).then(res => res.json()).then(function (data) {  //фуункция получения json
    for (key in data['objects']) {
        var sel = document.getElementById('address')
        var opt = document.createElement('option')
        if (data['objects'][key]['flat'] == null) {
            var room = '';
        } else {
            room = ', кв. ' + data['objects'][key]['flat']
        }
        opt.innerHTML = data['objects'][key]['address'] + room;
        sel.appendChild(opt);
    }
});