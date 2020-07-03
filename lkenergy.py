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
    if session == {}:
        return redirect('/')
    return render_template('main.html')


@app.route('/get_json_obj', methods=['POST', 'GET'])
def get_jsn():
    id = session['id']
    query = "SELECT b.address, o.flat FROM buildings AS b JOIN objects AS o ON b.id = o.buildingId WHERE b.id IN " \
            "(SELECT buildingID FROM objects WHERE userId = %d)" % id
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
    return redirect('/')


@app.route('/adder', methods=['POST', 'GET'])
def adder():
    if session == {}:
        return redirect('/')
    if request.method == "POST":
        address = request.form['hidden_address']
        room = request.form['hidden_room']
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


# @app.route('/admin', methods=['POST', 'GET'])
# def admin():
#     if session.get('isAdmin') == None:
#         return redirect('/')
#     return render_template('admin.html')


@app.route('/requests', methods=['POST', 'GET'])
def requests():
    if session.get('isAdmin') == None:
        return redirect('/')
    return render_template('requests.html')


@app.route("/json_request", methods=['POST', 'GET'])
def json_request():
    query = "SELECT r.id, r.userId, r.buildingId, r.flat, u.name, b.address FROM requests AS r JOIN buildings AS b " \
            "ON r.BuildingId = b.id JOIN users AS u ON r.userId = u.id"
    print(query)
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


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
