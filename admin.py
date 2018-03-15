from flask import Flask,render_template,request,redirect,url_for
import sqlite3


app = Flask(__name__)

@app.route('/validcourse',methods= ["Post","Get"])
def validcourse():
    if request.method == 'POST':
        try:
            Course = request.form['CourseId']
            Name = request.form['CourseName']
            FID = request.form['FID']
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO CourseTable (CourseId, CourseName) VALUES(?, ?)",(Course,Name))
            conn.commit()
            msg = "Recorded Updated sucessfully"
        except:
            conn.rollback()
            msg = "Error updating record"
        return redirect(url_for('addcourses', name=msg))

@app.route('/')
@app.route('/<name>')
def index(name=None):
    return render_template('adminhomepage.html',text=name)


@app.route('/validadmin',methods = ['POST', 'GET'])
def validadmin():
    user = request.form['UserName']
    pwd = request.form['Password']
    print(pwd)
    if not user or not pwd:
        error = "Any of the fields cannot be left blank"
        return redirect(url_for('index', name=error))
    if user != "admin":
        error = "UserName is incorrect!"
        return redirect(url_for('index', name=error))

    else:
        if pwd == "thisispassword":
            return redirect(url_for('addcourses'))
        else:
            error = "Password is incorrect!"
            return redirect(url_for('index', name=error))

@app.route('/addcourses')
@app.route('/addcourses/<name>')
def addcourses(name=None):
    return render_template("addcourses.html",text=name)


@app.route('/forgotpassword')
def forgotpassword():
    error = "Contact system administrator"
    return redirect(url_for('index', name=error))

soft.secret_key = 'database.db'

if __name__ == '__main__':
    app.run(debug=True,port=5500)