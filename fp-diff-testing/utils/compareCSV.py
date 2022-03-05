import csv
import sys

def readInCsv(fileName):
  with open(fileName) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    currClass = 0
    functions = []
    dictionary = {}
    for row in csv_reader:
      if line_count != 0:
        if int(row[0]) == currClass:
          functions.append(row[1])
        else:
          functions.sort()
          dictionary[functions[0]] = functions
          functions = []
          functions.append(row[1])
          currClass = int(row[0])
      line_count += 1
    functions.sort()
    dictionary[functions[0]] = functions
  return dictionary

def compareTwoDict(dictionary1, dictionary2, str1, str2):
  for key in dictionary1:
    if key not in dictionary2:
      print("Class found in {} but not in {} : {}".format(str1, str2, dictionary1[key]))

def findDiscrepancies(dictionary1, dictionary2, str1, str2):
  pairs = []
  for key in dictionary1:
    if key in dictionary2:
      if dictionary1[key] != dictionary2[key]:
        print("This class is slightly different: {} {}".format(str1, dictionary1[key]))
        print("                                  {} {}".format(str2, dictionary2[key]))

if __name__ == "__main__":
  newFile = sys.argv[1]
  oldFile = sys.argv[2]
  dictionary_new = readInCsv(newFile)
  dictionary_old = readInCsv(oldFile)
  compareTwoDict(dictionary_new, dictionary_old, newFile, oldFile)
  compareTwoDict(dictionary_old, dictionary_new, oldFile, newFile)
  findDiscrepancies(dictionary_new, dictionary_old, newFile, oldFile)
  