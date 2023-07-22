from flask import Flask,render_template,request,session,redirect,url_for
import mysql.connector

connection = mysql.connector.connect(host='localhost',port='3307',
                                         database='trinityregistration',
                                         user='root',
                                         password='mysql')

cursor = connection.cursor()
app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template('home.html',username= session['username'])

@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM user WHERE username=%s AND password=%s',(username,password,))
        record = cursor.fetchone()
        if record:
            session['loggedin']= True
            session['username']= record[1]
            return redirect(url_for('home'))
        else:
            msg='Incorrect username/password.Try again!'
    return render_template('index.html',msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('login'))

@app.route("/python")
def python():
    cursor.execute("select * from reg_member where course='Python'")
    value=cursor.fetchall()
    return render_template("registration.html",data=value,name='Python')

@app.route("/java")
def java():
    cursor.execute("select * from reg_member where course='Java'")
    value=cursor.fetchall()
    return render_template("registration.html",data=value,name='Java')

@app.route("/c++")
def cplus():
    cursor.execute("select * from reg_member where course='C++'")
    value=cursor.fetchall()
    return render_template("registration.html",data=value,name='C++')

if __name__ == "__main__":
    app.run(debug=True)
