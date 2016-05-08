import downloadDB
import csv

def inputData(inData):
   f = open('../csvFiles/InputFile.csv', 'w')
   f.write(inData)
   
def checkHeader():
   headerMatches = True
   header = downloadDB.getHeader()
   with open("../csvFiles/InputFile.csv", 'rb') as csvFile:
      inData = csv.reader(csvFile)
      row = inData.next()
      if len(header) == len(row):
         for i in range(0, len(header)):
            if row[i] != header[i]:
               headerMatches = False
      else:
         headerMatches = False
   return headerMatches
   