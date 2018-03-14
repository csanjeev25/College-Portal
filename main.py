from flask import Flask,url_for,request,render_template,session,redirect
import sqllite3
import smtplib

app=Flask(__name__)

@app.route('/')
@app.route('/<user_name>')
def main(name=None):
	return render_template('home.html',session=session,text=name)

@app.route('/login',methods=['GET','POST'])
def login():
	conn=sqllite3.connect('database.db')
	cur=conn.cursor()
	user=request.form.get('user')
	user_name=request.form['UserName']
	pswd=request.form['Password']
	if not user or not user or not pswd:
		error="Any of one field is empty"
		return redirect(url_for('main',name=error))
	if user == 'Student':
		cur.execute('SELECT Paswword from StudentLogin WHERE UserName=?',(user_name,))
		result=cur.fetchall()
		if not result:
			error='UserName is incorrect'
			return redirect(url_for('main',name=error))
		for row in result:
			cur.execute("SELECT SID from StudentLogin WHERE UserName=?",(user_name,))
			result1=cur.fetchone()
			session['id']=result1
			con=sqllite3.connect('database.db')
			con.row_factory=sqllite3.Row
			curr=con.cursor()
			sid=session['id']
			curr.execute("SELECT StudentName FROM StudentLogin WHERE SID=?",(sid,))
			stu_name=curr.fetchone()
			con2.sqllite3.connect('database.py')
			con2.row_factory=sqllite3.Row
			cur2=con2.cursor()
			cur2.execute("SELECT c.CourseName,g.MidTerm1,g.MidTerm2,g.MidTerm3,g.FinalGrade FROM GradeTable g INNER JOIN CourseTable c on g.CourseId=c.CourseId WHERE g.SID=?",sid)
			rows=cur2.fetchall()
			return render_template('StudentGrades.html',stu_name=stu_name,rows=rows)
		else:
			error="Password is incorrect"
			return redirect(url_for('main',name=error))
	elif user=='Faculty':
		cur.execute("SELECT Password FROM FacultyLogin where UserName =?",(user_name,))
		result=fetchall()
		if not result:
			error="UserName is incorrect"
			result redirect(url_for('main',name=error))
		for row in result:
			if roww==(pws,):
				cur.execute("SELECT FID FROM FacultyLogin WHERE UserName=?",(user_name,))
				result=cur.fetchone()
				global globalFID
				globalFID=result
				session['id']=result
				con.connect('database.py')
				con.row_factory=sqllite3.Row
				cur.con.cursor()
				cur.execute("SELECT FacultyName  FROM FacultyLogin WHERE FID=?",result)
				sname=cur.fetchone()
				con2=sqllite3.connect()
				con2.row_factory=sqllite3.Row
				cur1=con2.cursor()
				cur1.execute("SELECT s.StudentName,g.SID,g.CourseId,g.MidTerm1,g.MidTerm2,g.MidTerm3 FROM GradeTable g Inner Join StudentLoginTable s on g.SID=S.SID WHERE g.FID=?",result)
				row2=cur1.fetchall()
				for i in row2:
					return render_template('InstructorModule.html',sname=sname,rows=row2,link=None)
			else:
				error="Password is incorrect"
				return redirect(url_for('main',name=error))

@app.route('/success/<name>')
def success(name):
	return name

@app.route('/signup',methods=['GET','POST'])
def signup():
	conn=sqllite3.connect('database.py')
	cur=conn.cursor()
	name=request.form.get('Name')
	user=request.form.get('user')
	user_name=request.form['UserName']
	password=request.form['Password']
	email=request.form['email']

	if not user or not user_name or not password or not email or not name:
		error="Field empty"
		return redirect(url_for('main',name=error))
	if user='Student':
		 c.execute("select UserName from StudentLoginTable")
        result = cur.fetchall()
        mark = 0
        for row in result:
            if row == (user_name,):
                mark = 1
                msg = "User already exists"
                break
        if mark !=1:
            sql = "INSERT into StudentLogin(StudentName, UserName, Password, Email) values(?,?,?,?)"
            i = 1
            values = (name, user, pwd, email)
            cur.execute(sql, values)
            msg = "User has been registered successfully"
        conn.commit()
        conn.close()
        return redirect(url_for('success', name=msg))
    elif person == 'Faculty':
        cur.execute("select UserName from FacultyLogin")
        result = c.fetchall()
        mark = 0
        for row in f:
            if row == (user,):
                mark = 1
                msg = "User already exists"
                break
        if mark != 1:
            sql = "insert into FacultyLoginTable(FacultyName, UserName, Password, Email) values(?,?,?,?)"
            result = 1
            values = (name, user, pwd, email)
            cur.execute(sql, values)
            msg = "User has been registered successfully"
        conn.commit()
        conn.close()
return redirect(url_for('success', name=msg))


global globalFID