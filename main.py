from flask import Flask, redirect, url_for, request,render_template,session
app = Flask(__name__)
import smtplib
import sqlite3

@app.route('/')
@app.route('/<name>')
def index(name=None):
    return render_template('HomePage.html',session=session,text=name)

@app.route('/success/<name>')
def success(name):
    return name

@app.route('/signuppage')
def signuppage():
   return render_template('SignUp.html')

@app.route('/forgotpassword')
@app.route('/forgotpassword/<name>')
def forgotpassword(name=None):
   return render_template('Forgot.html',text=name)

@app.route('/login',methods = ['POST', 'GET'])
def login():
    conn = sqlite3.connect('database.py')
    c = conn.cursor()
    SIDtopass = 0
    person = request.form.get('person','')
    user = request.form['UserName']
    pwd = request.form['Password']
    if not person or not user or not pwd:
        error = "Any of the fields cannot be left blank"
        return redirect(url_for('index', name=error))
    if person == 'Student':
        c.execute("select Password from StudentLoginTable where UserName = ?",(user,))
        f = c.fetchall()
        if not f:
            error = "UserName is incorrect!"
            return redirect(url_for('index', name=error))
        for row in f:
            if row == (pwd,):
                c.execute("select SID from StudentLoginTable where UserName = ?",(user,))
                f = c.fetchone()
                session['id']=f;
                con = sqlite3.connect('database.db')
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                sid = session['id']
                cur.execute("SELECT StudentName as sn FROM StudentLoginTable WHERE SID=?", sid)
                sname1 = cur.fetchone()
                con1 = sqlite3.connect('database.db')
                con1.row_factory = sqlite3.Row
                cur1 = con1.cursor()
                cur1.execute(
                    "SELECT c.CourseName as cn,g.MidTerm1 as mt1,g.MidTerm2 as g.MidTerm3 as mt3,g.FinalGrade as fg FROM GradeTable g Inner Join CourseTable c on g.CourseId=c.CourseId WHERE g.SID=?",
                    sid)
                rows = cur1.fetchall()
                return render_template('StudentGrades.html',sname=sname1,rows=rows)

            else:
                error = "Password is incorrect!"
                return redirect(url_for('index', name=error))
    elif person == 'Faculty':
        c.execute("select Password from FacultyLoginTable where UserName = ?", (user,))
        f = c.fetchall()
        if not f:
            error = "UserName is incorrect!"
            return redirect(url_for('index', name=error))
        for row in f:
            if row == (pwd,):
                c.execute("select FID from FacultyLoginTable where UserName = ?", (user,))
                f = c.fetchone()
                global globalFID
                globalFID = f
                session['id']=f
                fid = session['id']
                con = sqlite3.connect('database.db')
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT FacultyName as fn FROM FacultyLoginTable WHERE FID=?", fid)
                sname2 = cur.fetchone()
                con1 = sqlite3.connect('database.db')
                con1.row_factory = sqlite3.Row
                cur1 = con1.cursor()
                cur1.execute(
                    "SELECT s.StudentName as sn,g.SID as sid,g.CourseId as crid,g.MidTerm1 as mt1,g.MidTerm2 as mt2,g.MidTerm3 as mt3,g.FinalGrade as fg FROM GradeTable g Inner Join StudentLoginTable s on g.SID=S.SID WHERE g.FID=?",
                    fid)
                rows2 = cur1.fetchall()
                return render_template('Instructormodule.html', sname=sname2, rows=rows2,link=None)

            else:
                error = "Password is incorrect!"
                return redirect(url_for('index', name=error))


@app.route('/facultylogindisplay/<fidvalue>')
def facultylogindisplay(fidvalue):
    session['id'] = fidvalue
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    fi = int(fidvalue[0])
    cur.execute("SELECT FacultyName as fn FROM FacultyLoginTable WHERE FID=?", fi)
    sname2 = cur.fetchone()
    con1 = sqlite3.connect('database.db')
    con1.row_factory = sqlite3.Row
    cur1 = con1.cursor()
    cur1.execute(
        "SELECT s.StudentName as sn,g.SID as sid,g.CourseId as crid,g.MidTerm1 as mt1,g.MidTerm2 as mt2,g.MidTerm3 as mt3,g.FinalGrade as fg FROM GradeTable g Inner Join StudentLoginTable s on g.SID=S.SID WHERE g.FID=?",
        fi)
    rows2 = cur1.fetchall()
    return render_template('Instructormodule.html', sname=sname2, rows=rows2,a=None,b=None,c=None)


@app.route('/forgothandling',methods = ['POST', 'GET'])
def forgothandling():
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    email = request.form['Email']
    person = request.form.get('person', '')
    if not email or not person:
        error = "Any of the fields cannot be left blank"
        return redirect(url_for('forgotpassword', name=error))
    if person == 'Student':
        c.execute("select Password from StudentLoginTable where email = ?", (email,))
        f = c.fetchone()
        if not f:
            error = "Email entered is incorrect!"
            return redirect(url_for('forgotpassword', name=error))
        else:
            to = email
            gmail_user = ''
            gmail_pwd = ''
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(gmail_user, gmail_pwd)
            header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Confidential Message \n'
            msg = header + '\n This message contains your password to College Portal \n\n' + str(f[0])
            smtpserver.sendmail(gmail_user, to, msg)
            smtpserver.quit()
        message = "An Email containing password has been sent to your registered email ID"
        return redirect(url_for('forgotpassword', name=message))
    elif person == 'Faculty':
        c.execute("select Password from FacultyLoginTable where Email = ?", (email,))
        f = c.fetchall()
        if not f:
            error = "Email entered is incorrect!"
            return redirect(url_for('forgotpassword', name=error))
        else:
            to = email
            gmail_user = ''
            gmail_pwd = ''
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(gmail_user, gmail_pwd)
            header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Confidential Message \n'
            msg = header + '\n This message contains your password to College Portal \n\n' + str(f)
            smtpserver.sendmail(gmail_user, to, msg)
            smtpserver.quit()
            message = "An Email containing password has been sent to your registered email ID"
            return redirect(url_for('forgotpassword', name=message))


@app.route('/updategrades', methods=['GET', 'POST'])
def updategrades():
    connection = sqlite3.connect(sqlite_file)
    cr = connection.cursor()
    cid=request.form.get('CourseId',0)
    sid=request.form.get('StudentId',0)
    mt1x=request.form.get('MidTerm1',0)
    mt2x=request.form.get('MidTerm2',0)
    mt3x=request.form.get('MidTerm3',0)
    fgx=request.form.get('FinalGrades','A')
    global globalSID
    global globalFID
    task = (mt1, mt2, mt3, fg, sid, globalFID[0], cid)
    sql = "update GradeTable set MidTerm1 = ?, MidTerm2 = ?, MidTerm3 = ?, FinalGrade = ? where SID = ? and FID = ? and CourseId = ?"
    cr.execute(sql,task)
    a = cr.rowcount
    if a == 0:
        return 'The student didnot register the course'
    else:
        connection.commit()
        connection.close()
        con = sqlite3.connect('database.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        z = session['id']
        cur.execute("SELECT FacultyName as aa FROM FacultyLoginTable WHERE FID=?", z)
        sname2 = cur.fetchone()
        con1 = sqlite3.connect('database.db')
        con1.row_factory = sqlite3.Row
        cur1 = con1.cursor()
        cur1.execute(
        "SELECT s.StudentName as sn,g.SID as sid,g.CourseId as crid,g.MidTerm1 as mt1,g.MidTerm2 as mt2,g.MidTerm3 as mt3,g.FinalGrade as fg FROM GradeTable g Inner Join StudentLoginTable s on g.SID=S.SID WHERE g.FID=?",
        z)
        rows2 = cur1.fetchall()
        return render_template('Instructormodule.html', sname=sname2, rows=rows2, link=None)


@app.route('/callhtml/<a>/<b>/<c>/<d>/<e>' , methods=['GET', 'POST'])
def callhtml(a,b,c,d,e):
    return render_template('update.html',a=a,b=b,c=c,d=d,e=e)


@app.route('/clear')
def clearsession():
    session.clear()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    name = request.form['Name']
    person = request.form.get('person', '')
    user = request.form['UserName']
    pwd = request.form['Password']
    email = request.form['email']
    if not person or not user or not pwd or not email or not name:
        error = "Any of the fields cannot be left blank"
        return redirect(url_for('success', name=error))
    if person == 'Student':
        c.execute("select UserName from StudentLoginTable")
        f = c.fetchall()
        mark = 0
        for row in f:
            if row == (user,):
                mark = 1
                msg = "User already exists"
                break
        if mark !=1:
            sql = "insert into StudentLoginTable(StudentName, UserName, Password, Email) values(?,?,?,?)"
            i = 1
            values = (name, user, pwd, email)
            c.execute(sql, values)
            msg = "User has been registered successfully"
        conn.commit()
        conn.close()
        return redirect(url_for('success', name=msg))
    elif person == 'Faculty':
        c.execute("select UserName from FacultyLoginTable")
        f = c.fetchall()
        mark = 0
        for row in f:
            if row == (user,):
                mark = 1
                msg = "User already exists"
                break
        if mark != 1:
            sql = "insert into FacultyLoginTable(FacultyName, UserName, Password, Email) values(?,?,?,?)"
            i = 1
            values = (name, user, pwd, email)
            c.execute(sql, values)
            msg = "User has been registered successfully"
        conn.commit()
        conn.close()
        return redirect(url_for('success', name=msg))

global globalFID
app.secret_key = 'database.db'

if __name__ == '__main__':
    app.run(debug=True)


