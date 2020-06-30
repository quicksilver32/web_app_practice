from flask import Flask, render_template, request, redirect, url_for
import pyodbc
server = 'student-alan.database.windows.net'
database = 'StudentDB01'
username = 'team01'
password = 'Team11$%'
driver = '{ODBC Driver 13 for SQL Server}'
conn = pyodbc.connect('DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cur = conn.cursor()

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def check():
    if request.method == "POST":
        username = request.form['log']
        password = request.form['pass']
        query = "SELECT isCompany FROM users WHERE login = '%s' AND password = '%s'" % (username, password)
        cur.execute(query)
        row = cur.fetchone()
        if row:
            if row.isCompany:
                print('Company')
            else:
                print('Owner')
            return render_template('ok.html')
        else:
            print('No')
        return 'no'
    else:
        return render_template('auth.html')


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


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
