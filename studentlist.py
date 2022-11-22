import csv
import sys

def main():
  filename = sys.argv[1]
  students = []
  with open(filename) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
      wrd = row[0].split(',')
      if len(wrd) == 2:
        stName = f'{wrd[1]} {wrd[0]}'.strip()
        students.append(f'{stName}\n')
        
  with open('important_docs/myStudents.txt', 'w') as file1:
    file1.writelines(students)

if __name__ == "__main__":
  main()
