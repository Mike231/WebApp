import csv
import sys
from web import form
import psycopg2

conn_string = "host='0.0.0.0' dbname='students_db' user='postgres' password='postgres'"
db = psycopg2.connect(conn_string)
cursor = db.cursor()


###################################################################################
#Updates the classes from the header of the csv
def updateClass(inData):
    for classes in range(2, len(inData[0])):
        className = str(inData[0][classes])
        cursor.execute("INSERT INTO class(classname) VALUES(%(str)s);", {'str': className})
        
###################################################################################
#Updates the students in the database from the input csv
def updateStudent(inData):
    for line in range(1, len(inData)):
        lastname = inData[line][0]
        firstname = inData[line][1]
        cursor.execute("INSERT INTO student(lastname, firstname) VALUES(%s, %s);", (lastname, firstname))
        
###################################################################################
#Updates the grades in the database from the given csv
def updateGrade(inData):
    for i in range(1, len(inData)):
        for j in range(2, len(inData[i])):
            inGrade_Comment = inData[i][j].split(',')
            try:
                cursor.execute("INSERT INTO grade(lastname, classname, grade, comment) VALUES(%s, %s, %s, %s);", (inData[i][0], inData[0][j], inGrade_Comment[0], inGrade_Comment[1]))
            except IndexError:
                cursor.execute("INSERT INTO grade(lastname, classname, grade) VALUES(%s, %s, %s);", (inData[i][0], inData[0][j], inData[i][j]))
                
###################################################################################
#Call the functions to update the current database also clears out the current information in it
def doUpdate(csvfile):
    cursor.execute("DELETE FROM class;")
    cursor.execute("DELETE FROM student;")
    cursor.execute("DELETE FROM grade;")
    
    file = open(csvfile, "r")
    inData = list(csv.reader(file))
    
    updateClass(inData)
    updateStudent(inData)
    updateGrade(inData)
    db.commit()

#doUpdate("../csvFiles/zeroDB.csv")