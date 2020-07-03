fetch('/json_request', {method: 'POST'}).then(res => res.json()).then(function (data) { //фуункция получения json
    console.log(data)
});