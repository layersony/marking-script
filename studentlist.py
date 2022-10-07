import csv

def main():
  students = []
  with open('student.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
      wrd = row[0].split(',')
      students.append(f'{wrd[1]} {wrd[0]}'.strip())
  print(students)

if __name__ == "__main__":
  main()