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
    print('/', session)
    if session:
        return redirect("/main")
    if request.method == "POST":
        username = request.form['log']
        password = request.form['pass']
        query = "SELECT isCompany, id FROM users WHERE login = '%s' AND password = '%s'" % (username, password)
        cur.execute(query)
        row = cur.fetchone()
        if row:
            if row.isCompany:
                print('Company')
            else:
                print('Owner')
            session['isCompany'] = row.isCompany
            session['id'] = row.id
            return redirect('/main')
        else:
            print('No')
        return 'no'
    else:
        return render_template('auth.html')


def auth():
    return render_template('auth.html')


@app.route('/main', methods=['POST', 'GET'])
def main():
    if session != {}:
        print('main', session)
        return render_template('ok.html')
    else:
        return redirect('/')


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
            obj[count].update({'address': row[0] + row[1]})
        count += 1
    if request.method == "POST":
        return jsonify(obj)
    else:
        return render_template('ok.html')


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
        query = "SELECT id FROM users WHERE login = '%s'" % username
        cur.execute(query)
        row = cur.fetchone()
        print('1')
        if row:
            print('2')
            return "<h1>Login used</>"
        else:
            print('3')
            query = "INSERT INTO users (name, address, email, phone, isCompany, login, password)" \
                "VALUES('%s','%s','%s','%s',%s,'%s','%s')" % (name, address, email, phone, isCompany, username, password)
            cur.execute(query)
            conn.commit()
            return '<h1>Registrated</h1>'
    else:
        return render_template('registration.html')


@app.route("/log_out", methods=["GET"])
def log_out():
    session.pop('id', None)
    session.pop('isCompany', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
