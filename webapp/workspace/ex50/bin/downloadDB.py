import csv
import sys
from web import form
import psycopg2

conn_string = "host='0.0.0.0' dbname='students_db' user='postgres' password='postgres'"
db = psycopg2.connect(conn_string)
cursor = db.cursor()
    
###################################################################################
#Gets all the classes in the database
def getClassOrder():
    cursor.execute("SELECT * FROM class")
    len_c = len(cursor.fetchall())
    data = [0 for i in range(0, len_c)]
    with open("../csvFiles/zeroDB.csv", 'rb') as csvFile:
        inData = csv.reader(csvFile)
        row = inData.next()
        for i in range(0, len_c):
            data[i] = row[i+2]
    return data 
###################################################################################
#Gets all the current students in the database

def getStudents():
    cursor.execute("SELECT * FROM student;")
    s = cursor.fetchall()
    students = [0 for i in range(0, len(s))]
    for i in range(0, len(s)):
        students[i] = s[i]
    return students
    
###################################################################################
#Gets the header for the output csv

def getHeader():
    data = getClassOrder()
    cursor.execute("SELECT * FROM class ORDER BY %(str)s;", {'str': data})
    s = cursor.fetchall()
    header = [0 for i in range(0, len(s)+2)]
    header[0] = 'LastName'
    header[1] = 'FirstName'
    for i in range(0, len(s)):
        header[i+2] = s[i][0]
    return header
    
###################################################################################
#Gets all the grades of the every student in the database    

def getGrade():
    data = getClassOrder()
    students = getStudents()
    len_c = len(data)
    len_s = len(students)
    grades = [[0 for i in range(0, len_c)] for j in range(0, len_s)]
    for i in range(0, len_s):
        for j in range(0, len_c):
            cursor.execute("SELECT * FROM grade WHERE lastname = %(ln)s AND classname = %(str)s;",{'ln': students[i][0],'str': data[j]})
            d = cursor.fetchone()
            if d[3] != None:
                grades[i][j] = d[2]  + ", "+ d[3]
            else:
                grades[i][j] = d[2] + ", "
    return grades
    
###################################################################################    
#Dumps the current database into CurrentDatabaseCSV in the csvFiles to be used to download

def dumpDB(filename):
    with open("../csvFiles/"+filename+".csv", 'wb') as csvfile:
        fieldnames = getHeader()
        students = getStudents()
        grades = getGrade()
        student_array = [[0 for i in range(0, len(fieldnames))] for j in range(0, len(students))]
        for i in range(0, len(students)):
            student_array[i][0] = students[i][0]
            student_array[i][1] = students[i][1]
            student_array[i][2] = grades[i]
            temp = student_array[i][2]
            for j in range(2, len(fieldnames)):
                student_array[i][j] = temp[j-2]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer = csv.writer(csvfile)
        writer.writerows(student_array)
        
#dumpDB("Test")