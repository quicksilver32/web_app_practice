from flask import Flask, render_template, request, redirect, url_for
import pyodbc
server = 'student-alan.database.windows.net'
database = 'StudentDB01'
username = 'team01'
password = 'Team11$%'
driver = '{ODBC Driver 13 for SQL Server}'
conn = pyodbc.connect('DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cur = conn.cursor()
query = 'SELECT * FROM weekdays'
cur.execute(query)

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def test():
    if request.method == "POST":
        username = request.form['log']
        password = request.form['pas']
        query = "SELECT isCompany FROM users WHERE login = '%s' AND password = '%s'" % (username, password)
        cur.execute(query)
        row = cur.fetchone()
        if row:
            if row.isCompany:
                print('Company')
            else:
                print('Owner')
        else:
            print('No')
        return render_template('ok.html')
    else:
        return render_template('test.html')


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == "POST":
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['log']
        password = request.form['pas']
        isCompany = 1
        query = "SELECT id FROM users WHERE login = '%s'" % username
        cur.execute(query)
        row = cur.fetchone()
        if row:
            print('Login used')
            return "<h1>Хуй</>"
        query = "INSERT INTO users (name, address, email, phone, isCompany, login, password)" \
                "VALUES('%s','%s','%s','%s',%d,'%s','%s')" % (name, address, email, phone, isCompany, username, password)
        cur.execute(query)
        conn.commit()
        return '<h1>ЗБС</h1>'
    else:
        return render_template('reg.html')


if __name__ == "__main__":
    app.run(debug=True)