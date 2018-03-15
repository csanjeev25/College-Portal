import sqlite3

conn=sqlite3.connect('database.db')
cur=conn.cursor()


cur.execute("CREATE TABLE IF NOT EXISTS StudentLoginTable(SID INTEGER, StudentName TEXT, UserName TEXT, Password TEXT, Email TEXT,PRIMARY KEY(SID))")
cur.execute("CREATE TABLE IF NOT EXISTS FacultyLoginTable(FID INTEGER,FacultyName TEXT, UserName TEXT, Password TEXT, Email TEXT,PRIMARY KEY(FID))")
cur.execute("CREATE TABLE IF NOT EXISTS Gradetable(MidTerm1 REAL,MidTerm2 REAL,MidTerm3 REAL,FinalGrade REAL,SID INTEGER,CourseId INTEGER,FOREIGN KEY(SID) REFERENCES StudentLoginTable(SID),FOREIGN KEY(CourseId) REFERENCES CouseTable(CourseId),FID INTEGER,FOREIGN KEY(FID) REFERENCES FacultyLoginTable(FID)")
cur.execute("CREATE TABLE IF NOT EXISTS CouseTable(CourseId INTEGER,CourseName TEXT, PRIMARY KEY(CourseId))")

conn.commit()
conn.close()
