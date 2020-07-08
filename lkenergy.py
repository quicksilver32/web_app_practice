from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pyodbc
server = 'student-alan.database.windows.net'
database = 'StudentDB01'
username = 'team01'
password = 'Team11$%'
driver = '{ODBC Driver 13 for SQL Server}'
conn = pyodbc.connect('DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cur = conn.cursor()

app = Flask(__name__)
app.secret_key = "wowow"
session = {}


@app.route('/', methods=['POST', 'GET'])
def check():
    if session:
        if session.get('isAdmin') == None:
            return redirect('/main')
        else:
            return redirect("/requests")
    if request.method == "POST":
        username = request.form['log']
        password = request.form['pass']
        query = "SELECT id FROM admins WHERE login = N'%s' AND password = N'%s'" % (username, password)
        cur.execute(query)
        row = cur.fetchone()
        if row:
            session['isAdmin'] = True
            return redirect('/requests')
        query = "SELECT isCompany, id FROM users WHERE login = N'%s' AND password = N'%s'" % (username, password)
        cur.execute(query)
        row = cur.fetchone()
        if row:
            session['isCompany'] = row.isCompany
            session['id'] = row.id
            return redirect('/main')
        return 'no'
    else:
        return render_template('auth.html')


def auth():
    return render_template('auth.html')


@app.route('/main', methods=['POST', 'GET'])
def main():
    if session == {} or session.get('isAdmin'):
        return redirect('/')
    return render_template('main.html')


@app.route('/get_json_obj', methods=['POST', 'GET'])
def get_jsn():
    id = session['id']
    query = "SELECT b.address, o.flat FROM buildings AS b JOIN objects AS o ON b.id = o.buildingId WHERE b.id IN " \
            "(SELECT buildingID FROM objects WHERE userId = %d) AND o.userId = %d" % (id, id)
    cur.execute(query)
    rows = cur.fetchall()
    obj = {}
    count = 0
    for row in rows:
        obj.update({count: {}})
        if row[1] is None:
            obj[count].update({'type': 'Жилой дом'})
            obj[count].update({'address': row[0]})

        else:
            obj[count].update({'type': 'Квартира'})
            obj[count].update({'address': row[0] + ', кв.' + row[1]})
        count += 1
    if request.method == "POST":
        return jsonify(obj)
    else:
        return render_template('main.html')


@app.route('/registration', methods=['POST', 'GET'])
def reg():
    if request.method == "POST":
        name = request.form['UserName']
        address = request.form['UserAddress']
        email = request.form['UserEmail']
        phone = request.form['UserPhone']
        username = request.form['UserLogin']
        password = request.form['UserPass']
        isCompany = request.form['GridRadios']
        query = "SELECT id FROM users WHERE login = N'%s'" % username
        cur.execute(query)
        row = cur.fetchone()
        if row:
            return "<h1>Login used</>"
        else:
            query = "INSERT INTO users (name, address, email, phone, isCompany, login, password)" \
                "VALUES(N'%s',N'%s',N'%s',N'%s',%s,N'%s',N'%s')" % (name, address, email, phone, isCompany, username, password)
            cur.execute(query)
            conn.commit()
            return '<h1>Registrated</h1>'
    else:
        return render_template('registration.html')


@app.route("/logout", methods=["GET"])
def logout():
    session.pop('id', None)
    session.pop('isAdmin', None)
    session.pop('isCompany', None)
    session.pop('json_ajax', None)
    return redirect('/')


@app.route('/adder', methods=['POST', 'GET'])
def adder():
    if session == {} or session.get('isAdmin'):
        return redirect('/')
    if request.method == "POST":
        address = request.form['hidden_address']
        room = request.form['hidden_room']
        if address == '':
            return redirect('/adder')
        userId = session['id']
        if session ['isCompany']:
            query = "SELECT * FROM requests WHERE userID = N'%s' AND BuildingId = (SELECT id FROM buildings " \
                    "WHERE address = N'%s')" % (userId, address)
        else:
            query = "SELECT * FROM requests WHERE userID = N'%s' AND BuildingId = (SELECT id FROM buildings " \
                    "WHERE address = N'%s') AND flat = N'%s'" \
                    % (userId, address, room)
        cur.execute(query)
        row = cur.fetchone()
        if row:
            return redirect('/adder')
        if session ['isCompany']:
            query = "SELECT * FROM objects WHERE userID = N'%s' AND BuildingId = (SELECT id FROM buildings " \
                    "WHERE address = N'%s')" % (userId, address)
        else:
            query = "SELECT * FROM objects WHERE userID = N'%s' AND BuildingId = (SELECT id FROM buildings " \
                    "WHERE address = N'%s') AND flat = N'%s'" \
                    % (userId, address, room)
        cur.execute(query)
        row = cur.fetchone()
        if row:
            return redirect('/adder')
        if session['isCompany']:
            query = "INSERT INTO requests (userId, BuildingId)" \
                    "VALUES(N'%s', (SELECT id FROM buildings WHERE address = N'%s'))" % (userId, address)
        else:
            query = "INSERT INTO requests (userId, BuildingId, flat)" \
                    "VALUES(N'%s', (SELECT id FROM buildings WHERE address = N'%s'), N'%s')" % (userId, address, room)
        cur.execute(query)
        conn.commit()
        return redirect('/adder')
    else:
        return render_template('adder.html')


@app.route('/adder_json', methods=['POST', 'GET'])
def adder_json():
    if session == {}:
        return redirect('/')
    query = """SELECT address, room_count_live FROM buildings ORDER BY address """
    cur.execute(query)
    rows = cur.fetchall()
    buildings = {}
    count = 0
    for row in rows:
        buildings.update({count: {}})
        buildings[count].update({'address': row[0]})
        buildings[count].update({'room_count': row[1]})
        count += 1
    buildings.update({count: session['isCompany']})
    return jsonify(buildings)


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if session.get('isAdmin') == None:
        return redirect('/')
    return render_template('admin.html')


@app.route('/requests', methods=['POST', 'GET'])
def requests():
    if session.get('isAdmin') == None:
        return redirect('/')
    return render_template('requests.html')


@app.route("/json_request", methods=['POST', 'GET'])
def json_request():
    query = "SELECT r.id, r.userId, r.buildingId, r.flat, u.name, b.address FROM requests AS r JOIN buildings AS b " \
            "ON r.BuildingId = b.id JOIN users AS u ON r.userId = u.id"
    cur.execute(query)
    rows = cur.fetchall()
    requests = {}
    count = 0
    for row in rows:
        requests.update({count: {}})
        requests[count].update({'requestId': row.id})
        requests[count].update({'userId': row.userId})
        requests[count].update({'buildingId': row.buildingId})
        requests[count].update({'room': row.flat})
        requests[count].update({'userName': row.name})
        requests[count].update({'address': row.address})
        count += 1
    return jsonify(requests)


@app.route('/req_change')
def req_change():
    data = request.args.get('data')
    data = data.split('_')
    data[0] = int(data[0])
    data[1] = int(data[1])
    data[3] = int(data[3])
    if data[4] == 'accept':
        if data[2] == '':
            query = "INSERT INTO objects (userId, buildingId) VALUES (%d, %d)" % (data[0], data[1])
        else:
            query = "INSERT INTO objects (userId, buildingId, flat) VALUES (%d, %d, N'%s')" % (data[0], data[1], data[2])
        cur.execute(query)
        cur.commit()
    query = "DELETE FROM requests WHERE id=%d" % data[3]
    cur.execute(query)
    cur.commit()
    return redirect('/')


@app.route('/dashboard_admin', methods=['POST', 'GET'])
def dashboard_admin():
    if session.get('isAdmin') == None:
        return redirect('/')
    return render_template('dashboard_admin.html')


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if session == {} or session.get('isAdmin'):
        return redirect('/')
    return render_template('dashboard.html')


@app.route('/json_dashboard', methods=['POST', 'GET'])
def json_dashboard():
    userId = session['id']
    data = {'userId': userId, 'isCompany': session['isCompany']}
    data.update({'objects': {}})
    query = "SELECT b.address, o.buildingId, o.flat FROM objects AS o JOIN buildings AS b ON o.buildingId = b.id " \
            "WHERE o.userId = %d ORDER BY b.address" % userId
    cur.execute(query)
    rows = cur.fetchall()
    data.update({'objects': {}})
    count = 0
    for row in rows:
        data['objects'].update({count: {}})
        data['objects'][count].update({'buildingId': row.buildingId})
        data['objects'][count].update({'address': row.address})
        data['objects'][count].update({'flat': row.flat})
        count += 1

    return jsonify(data)


@app.route('/admin_json_dashboard', methods=['POST', 'GET'])
def admin_json_dashboard():
    data = {}
    data.update({'regions': {}})
    query = "SELECT id, name FROM regions ORDER BY name"
    cur.execute(query)
    rows = cur.fetchall()
    count = 0
    for row in rows:
        data['regions'].update({count: {}})
        data['regions'][count].update({'id': row.id})
        data['regions'][count].update({'name': row.name})
        count += 1

    data.update({'cities': {}})
    query = "SELECT id, name FROM cities ORDER BY name"
    cur.execute(query)
    rows = cur.fetchall()
    count = 0
    for row in rows:
        data['cities'].update({count: {}})
        data['cities'][count].update({'id': row.id})
        data['cities'][count].update({'name': row.name})
        count += 1

    data.update({'buildings': {}})
    query = "SELECT DISTINCT b.id, b.address, b.room_count_live, b.region_id, b.city_id FROM buildings AS b " \
            "JOIN objects AS o ON b.id = o.buildingId ORDER BY address"
    cur.execute(query)
    rows = cur.fetchall()
    count = 0
    for row in rows:
        data['buildings'].update({count: {}})
        data['buildings'][count].update({'id': row.id})
        data['buildings'][count].update({'address': row.address})
        data['buildings'][count].update({'room_count_live': row.room_count_live})
        data['buildings'][count].update({'region_id': row.region_id})
        data['buildings'][count].update({'city_id': row.city_id})
        count += 1
    query = "SELECT b.address, c.flat  FROM customers AS c JOIN buildings AS b ON c.buildingId = b.id " \
            "WHERE c.buildingid in (SELECT DISTINCT buildingid FROM objects) " \
            "AND c.PeopleCount != '-1' AND c.flat != '-1' " \
            "ORDER BY b.address, c.flat"
    data.update({'rooms': {}})
    cur.execute(query)
    rows = cur.fetchall()
    rooms = set()
    for row in rows:
        rooms.add(row[0])
    rooms = dict.fromkeys(rooms, [])
    for row in rows:
        lst = list(rooms[row.address])
        lst.append(int(row.flat))
        rooms[row.address] = lst
    for room in rooms:
        rooms[room] = list(set(rooms[room]))
        rooms[room].sort()
    data['rooms'] = rooms
    return jsonify(data)


@app.route('/admin_obj_json', methods=['POST', 'GET'])
def admin_obj_json():
    query = "SELECT o.id, o.userId, o.buildingId, o.flat, u.name, b.address FROM objects AS o JOIN buildings AS b " \
            "ON o.buildingId = b.id JOIN users AS u ON o.userId = u.id ORDER BY u.name, b.address"
    cur.execute(query)
    rows = cur.fetchall()
    obj = {}
    count = 0
    for row in rows:
        obj.update({count: {}})
        obj[count].update({'objectId': row.id})
        obj[count].update({'userId': row.userId})
        obj[count].update({'buildingId': row.buildingId})
        obj[count].update({'room': row.flat})
        obj[count].update({'userName': row.name})
        obj[count].update({'address': row.address})
        count += 1
    return jsonify(obj)


@app.route('/obj_change')
def obj_change():
    data = int(request.args.get('data'))
    query = "DELETE FROM objects WHERE id=%d" % data
    cur.execute(query)
    cur.commit()
    return redirect('/')


@app.route('/json_ajax', methods=['POST', 'GET'])
def json_ajax():
    data = request.args.get('data')
    data = data.split('_')
    dk = {'address': data[0], 'start': data[1], 'end': data[2], 'checked': data[3]}
    session['json_ajax'] = dk
    return jsonify(dk)


@app.route('/json_ajax_data', methods=['POST', 'GET'])
def data_ajax():
    data ={}
    data.update({'type': session['json_ajax']['checked']})
    data.update({'data': {}})
    session['json_ajax']['start'] = session['json_ajax']['start'] + " 00:00:00"
    session['json_ajax']['end'] = session['json_ajax']['end'] + " 00:00:00"
    if session['json_ajax']['checked'] == '1':
        # ГИСТОРГРАММА ПО ПОТРЕБЛЕНИЮ ДОМОВ ЗА ОПР ПЕРИОД
        query = "SELECT SUM(md.Consumption) AS сonsumption, b.address, b.room_count_live FROM meter_data AS md " \
                "JOIN customers AS c ON md.CustomerId = c.id JOIN buildings as b ON md.BuildingId = b.id " \
                "WHERE md.BuildingId in (SELECT DISTINCT buildingId FROM objects WHERE userId = %d )" \
                " AND md.DT BETWEEN '%s' AND '%s' " \
                "GROUP BY b.address, b.room_count_live ORDER BY b.address" % (session['id'],
                                                                              session['json_ajax']['start'],
                                                                              session['json_ajax']['end'])
        cur.execute(query)
        rows = cur.fetchall()
        count = 0
        for row in rows:
            data['data'].update({count: {}})
            data['data'][count].update({'address': row.address})
            data['data'][count].update({'сonsumption': row.сonsumption})
            data['data'][count].update({'room_count': row.room_count_live})
            count += 1
    else:
        # ГРФИК + ТАБЛИЦА ПО ПОТРЕБЛЕНИЮ 1 ДОМА ЗА ПЕРИОД ПО ДНЯМ
        query = "SELECT SUM(md.Consumption) AS сonsumption, md.DT, b.room_count_live FROM meter_data AS md  " \
                "JOIN customers AS c ON md.CustomerId = c.id JOIN buildings as b ON md.BuildingId = b.id  " \
                "WHERE b.address = N'%s' AND md.DT BETWEEN '%s' AND '%s' " \
                "GROUP BY md.DT, b.room_count_live ORDER BY md.DT" % (session['json_ajax']['address'],
                                                                      session['json_ajax']['start'],
                                                                      session['json_ajax']['end'])
        cur.execute(query)
        rows = cur.fetchall()
        count = 0
        for row in rows:
            data['data'].update({count: {}})
            data['data'][count].update({'dt': row.DT})
            data['data'][count].update({'сonsumption': row.сonsumption})
            data['data'][count].update({'room_count': row.room_count_live})
            count += 1
    return jsonify(data)


@app.route('/json_admin_dashboard', methods=['POST', 'GET'])
def json_admin_dashboard():
    data = request.args.get('data')
    data = data.split('_')
    if len(data) == 5:
        admin_json = {"address": data[0], 'room': data[1], 'start': data[2], 'end': data[3], 'radio': data[4]}
        session['json_ajax'] = admin_json
    else:
        admin_json = {"address": data[0], 'start': data[1], 'end': data[2], 'radio': data[3]}
        session['json_ajax'] = admin_json
    print(session['json_ajax'])
    return jsonify(session['json_ajax'])


@app.route('/get_json_admin_dashboard', methods=['POST', 'GET'])
def get_json_admin_dashboard():
    data = {}
    session['json_ajax']['start'] = session['json_ajax']['start'] + " 00:00:00"
    session['json_ajax']['end'] = session['json_ajax']['end'] + " 00:00:00"
    data.update({'type': session['json_ajax']['radio']})
    data.update({'data': {}})
    if session['json_ajax']['radio'] == '0':
        query = "SELECT b.address, SUM(md.Consumption) AS consumption, b.room_count_live  " \
                "FROM meter_data AS md JOIN buildings AS b ON md.BuildingId=b.id " \
                "JOIN regions AS r ON b.region_id= r.id " \
                "WHERE r.name = N'%s' " \
                "AND md.DT BETWEEN '%s' AND '%s' " \
                "GROUP BY b.address, b.room_count_live ORDER BY b.address" % (session['json_ajax']['address'],
                                                                              session['json_ajax']['start'],
                                                                              session['json_ajax']['end'])
        print(query)
        cur.execute(query)
        rows = cur.fetchall()
        count = 0
        for row in rows:
            data['data'].update({count: {}})
            data['data'][count].update({'address': row.address})
            data['data'][count].update({'сonsumption': row.consumption})
            data['data'][count].update({'room_count': row.room_count_live})
            count += 1
    if session['json_ajax']['radio'] == '1':
        query = "SELECT b.address, SUM(md.Consumption) AS consumption, b.room_count_live  " \
                "FROM meter_data AS md JOIN buildings AS b ON md.BuildingId=b.id " \
                "JOIN cities AS c ON b.city_id= c.id " \
                "WHERE c.name = N'%s' " \
                "AND md.DT BETWEEN '%s' AND '%s' " \
                "GROUP BY b.address, b.room_count_live ORDER BY b.address" % (session['json_ajax']['address'],
                                                                              session['json_ajax']['start'],
                                                                              session['json_ajax']['end'])
        cur.execute(query)
        rows = cur.fetchall()
        count = 0
        for row in rows:
            data['data'].update({count: {}})
            data['data'][count].update({'address': row.address})
            data['data'][count].update({'сonsumption': row.consumption})
            data['data'][count].update({'room_count': row.room_count_live})
            count += 1
    if session['json_ajax']['radio'] == '2':
        query = "SELECT c.flat , SUM(md.Consumption) AS consumption, c.PeopleCount  " \
                "FROM meter_data AS md JOIN buildings AS b ON md.BuildingId=b.id " \
                "JOIN customers AS c ON md.CustomerId=c.id " \
                "WHERE b.address = N'%s' " \
                "AND md.DT BETWEEN '%s' AND '%s' " \
                "AND c.PeopleCount != '-1' AND c.flat != '-1' " \
                "GROUP BY c.flat, c.PeopleCount ORDER BY c.flat" % (session['json_ajax']['address'],
                                                                    session['json_ajax']['start'],
                                                                    session['json_ajax']['end'])
        cur.execute(query)
        rows = cur.fetchall()
        count = 0
        for row in rows:
            data['data'].update({count: {}})
            data['data'][count].update({'address': row.flat})
            data['data'][count].update({'сonsumption': row.consumption})
            data['data'][count].update({'room_count': row.PeopleCount})
            count += 1
    if session['json_ajax']['radio'] == '3':
        query = "SELECT SUM(md.Consumption) AS сonsumption, md.DT, c.flat, c.PeopleCount " \
                "FROM meter_data AS md  JOIN customers AS c ON md.CustomerId = c.id " \
                "JOIN buildings as b ON md.BuildingId = b.id  " \
                "WHERE b.address = N'%s' AND c.flat = N'%s' " \
                "AND md.DT BETWEEN '%s' AND '%s' " \
                "GROUP BY md.DT, c.flat, c.PeopleCount " \
                "ORDER BY c.flat, md.DT" % (session['json_ajax']['address'],
                                            session['json_ajax']['room'],
                                            session['json_ajax']['start'],
                                            session['json_ajax']['end'])
        cur.execute(query)
        rows = cur.fetchall()
        count = 0
        for row in rows:
            data['data'].update({count: {}})
            data['data'][count].update({'room': row.flat})
            data['data'][count].update({'сonsumption': row.сonsumption})
            data['data'][count].update({'people_count': row.PeopleCount})
            data['data'][count].update({'dt': row.DT})
            count += 1
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
