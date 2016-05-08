import web
from web import form
import sys
import os
import Image
import psycopg2
import downloadDB
import adviseBox
import updateDB
import processInCSV
urls = (
	'/', 'index',
	'/logout', 'logout',
	'/students', 'students',
	'/advise', 'advise',
	'/upload', 'upload',
)

app = web.application(urls, globals())
conn_string = "host='0.0.0.0' dbname='students_db' user='postgres' password='postgres'"

#C9 instructions into database
#sudo service postgresql start
#sudo su - postgres
#psql students_db
#pw postgres

###################################################################################
#Starts the session with the requirements for the Webpy webframework
render = web.template.render('../templates/')
if web.config.get('_session') is None:
	session = web.session.Session(app, web.session.DiskStore('sessions'),
		initializer={'users': 'anonymous'})
	web.config._session = session
else:
	session = web.config._session
	
db = psycopg2.connect(conn_string)
cursor = db.cursor()


###################################################################################
#Handles the information to send and recieve from the index page
class index:
	global login_form
	login_form = form.Form(
		form.Textbox('Username', form.notnull, descrpition='Username:'),
		form.Password('Password', form.notnull, descrpition='Password:'),
		)
		
	def GET(self):
		return render.index(login_form(), False)
		
	def POST(self):
		data = web.input()
		name = data.Username
		password = data.Password
		cursor.execute("SELECT * FROM users WHERE username = %(username)s",{'username': name})
		record = cursor.fetchone()
		if record != None:
			if name == record[1]:
				if password == record[1]:
					cursor.execute("SELECT * FROM student ORDER BY lastname ASC")
					dbStudents = cursor.fetchall()
					return render.students(dbStudents)
					
		return render.index(login_form(), True)
		
		

###################################################################################
#Handles the information to send and recieve from the students page
class students:
	def GET(self):
		data = web.input()
		student_Name = str(data.student)
		return students.getPage(self, student_Name)
		
		
	def POST(self):
		data = web.input()
		buttonType = data.button_type
		inData = data.in_Data
		className = data.class_name
		inName = data.student_name
		
		if buttonType == "G":
			students.inputGrade(self, inData, inName, className)
			
		if buttonType == "C":
			students.inputComment(self, inData, inName, className)
			
		return students.getPage(self, data.student_name)
		
	def inputGrade(self, in_grade, in_name, in_class):
		cursor.execute("UPDATE grade SET grade = %s WHERE lastname = %s AND classname = %s;", (in_grade, in_name, in_class))
		db.commit()
		
	
	def inputComment(self, in_comment, in_name, in_class):
		cursor.execute("UPDATE grade SET comment = %s WHERE lastname = %s AND classname = %s;", (in_comment, in_name, in_class))
		db.commit()
		
		
	def getPage(self, s_name):
		cursor.execute("SELECT * FROM grade WHERE lastname = %(lastname)s ORDER by classname ASC;",{'lastname': s_name})
		grades = cursor.fetchall()
		mylist = [0 for i in range(len(grades))]
		for i in range(len(grades)):
			temp = grades[i]
			mylist[i] = adviseBox.getButton(s_name, temp[1], temp[2], temp[3]) 
		return render.advise(mylist)
		
###################################################################################		
#Handles the information to send and recieve from the upload page
class upload:
	def GET(self):
		downloadDB.dumpDB("CurrentDatabaseCSV")
		return render.upload(False)
		
	def POST(self):
		inCSV = web.input()
		inData = inCSV.userfile
		processInCSV.inputData(inData)
		if processInCSV.checkHeader():
			updateDB.doUpdate("../csvFiles/InputFile.csv")
			cursor.execute("SELECT * FROM student ORDER BY lastname ASC")
			dbStudents = cursor.fetchall()
			return render.students(dbStudents)
		else:
			return render.upload(True)
			
###################################################################################
#Handles the information to send and recieve from the advise page
class advise:
	def GET(self):
		cursor.execute("SELECT * FROM student ORDER BY lastname ASC")
		dbStudents = cursor.fetchall()
		return render.students(dbStudents)
		
###################################################################################	
#Handles the information to end the session of the app
class logout:
	def GET(self):
		session.kill()
		raise web.seeother('/')
		
###################################################################################		
if __name__ == "__main__":
	app.run()