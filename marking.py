import json
import codecs
import os
from bs4 import BeautifulSoup
import subprocess
import csv
import time
from time import gmtime, strftime
from json.decoder import JSONDecodeError
from subprocess import Popen, PIPE

class bcolors:
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'

def newInstance(labname, studentId, name, gitname, status, msg):
  data = [studentId, name, gitname, status, msg]
  with open(f'{labname}.csv', 'a', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data)

def getMyStudents() -> list:
  myStudents = []
  with open('important_docs/myStudents.txt', 'r') as f:
    for i in f.readlines():
      myStudents.append(' '.join(i.split()))
  return myStudents

def createheader(labname):
  header = ['Id', 'Student Name', 'Git Name', 'Status', 'Message']
  with open(f'{labname}.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

# mark those with RSPEC
def rspecMark(params) -> str:
  """
  Clones & runs rspecfile
  :return: path for this.json file
  """
  # sSave test result in this.json file
  subprocess.run(f"cd {params.get('studentUsername')}; git clone {params.get('gitlink')}; cd {params.get('gitRepoName')}; rspec -f j -o this.json", shell=True)
  pathThisJson = f"{os.getcwd()}/{params.get('studentUsername')}/{params.get('gitRepoName')}/this.json"
  return pathThisJson

# mark those with gemfile
def bundleMark(params) -> str:
  """
  Clones & runs learn test
  :return: path for this.json file
  """
  subprocess.run(f"cd {params.get('studentUsername')}; git clone {params.get('gitlink')}; cd {params.get('gitRepoName')}; bundle install --retry=3; learn test -o this; cp .results.json this.json", shell=True)
  pathThisJson = f"{os.getcwd()}/{params.get('studentUsername')}/{params.get('gitRepoName')}/this.json"
  return pathThisJson

# mark those with npm
def npmMark(params) -> str:
  """
  Clones & runs learn test
  :return: path for this.json file
  """
  subprocess.run(f"cd {params.get('studentUsername')}; git clone {params.get('gitlink')}; cd {params.get('gitRepoName')};npm install; npm test; cp .results.json this.json", shell=True)
  pathThisJson = f"{os.getcwd()}/{params.get('studentUsername')}/{params.get('gitRepoName')}/this.json"
  return pathThisJson

def reactnpmMark(params) -> str:
  """
  Clones & runs learn test
  :return: path for this.json file
  """
  subprocess.run(f"cd {params.get('studentUsername')}; git clone {params.get('gitlink')}; cd {params.get('gitRepoName')};npm install; npm i npm test; cp .results.json this.json", shell=True)
  pathThisJson = f"{os.getcwd()}/{params.get('studentUsername')}/{params.get('gitRepoName')}/this.json"
  return pathThisJson

# mark those with learn

def main(labname, testType, myStudents, phrase):
  lenFiles = len(os.listdir(f"{os.getcwd()}/submissions"))
  currStud = 1
  for filename in os.listdir(f"{os.getcwd()}/submissions"):
    # skip files that starts with . eg .dist
    studentId = int(filename.split("_")[1])
    if not filename.startswith('.'):
      f = codecs.open(f"submissions/{filename}", "r", "utf-8")
      content = f.read()
      beautifulSoupText = BeautifulSoup(content, 'lxml')

      # students Details
      sname = beautifulSoupText.find('h1').text.strip().split(':')[-1].strip()
      status = None
      msg = None

      # get github repo link
      for a in beautifulSoupText.find_all('a', href=True):
        glink = a['href']

      try:
        gitSplit = glink.split('/')
        studentUsername = gitSplit[3]
        gitlink = "/".join(gitSplit[:5]).split('?')[0].split('#')[0]

        gitRepoName = gitSplit[4].split('.')[0].split('?')[0].split('#')[0]
  

        if sname in myStudents:
          print(f"{currStud} / {lenFiles}")
          currStud+=1
          print(studentUsername)
          # creates folder for student
          subprocess.run(["mkdir", f"{studentUsername}"])

          if phrase not in gitSplit[4]:
            status = "Incomplete"
            msg = "Submit the correct Lab"
          elif "fis-wip" in gitSplit or "commit" in gitSplit or "fis-whip" in gitSplit:
            status = "Incomplete"
            msg = "Push your Code to the Master or Main Branch"
          else:
            if len(gitSplit) == 5 or "master" in gitSplit or "main" in gitSplit:
              params = {
                  "studentUsername": studentUsername,
                  "gitlink": gitlink,
                  "gitRepoName": gitRepoName
              }
              try:
                # marking starts
                if testType.lower() == 'rspec':
                  filepath = rspecMark(params)
                elif testType.lower() == 'bundle':
                  filepath = bundleMark(params)
                else:
                  filepath = npmMark(params)
              except KeyboardInterrupt:
                  continue


              try:
                with open(filepath) as f:
                  data = json.load(f)

                  if testType.lower() == 'npm':
                    # total number of examples
                    exampleCount = data["stats"]["tests"]
                    # failed number of examples
                    failureCount = data["stats"]["failures"]
                  else:
                    # total number of examples
                    exampleCount = data['summary']['example_count']
                    # failed number of examples
                    failureCount = data['summary']['failure_count']

                  if failureCount >= exampleCount/2:
                    status = "Incomplete"
                    msg = "Some Test Failed to Passed, Kindly Recheck and Resubmit"
                  else:
                    status = "Complete"
                    msg = "Good Work"
              except FileNotFoundError:
                status = "Incomplete"
                msg = "Do recheck your work and resubmit it, Make sure the tests are working"
              except JSONDecodeError as e:
                status = "Incomplete"
                msg = "Json File has malfunctioned"

          # new instance
          newInstance(labname, studentId, sname, gitSplit[3], status, msg)
          subprocess.run(f"rm -rf {os.getcwd()}/{studentUsername}/", shell=True)
          print("="*60)
          
      except IndexError:
        pass

def codeChallenges():
  for filename in os.listdir(f"{os.getcwd()}/submissions"):
    print(filename)
    if filename.endswith(".bundle"):
      studentname = filename.split('_')[0]
      # creates folder for student
      subprocess.run(f"cd code_challenge; git clone {os.getcwd()}/submissions/{filename}", shell=True)

def cleanup(labname) -> any:
  subprocess.run(f"mv {os.getcwd()}/{labname}.csv  {os.getcwd()}/markedCsv", shell=True)
  # remove submissions folder
  subprocess.run(f"rm -rf {os.getcwd()}/submissions", shell=True)
  print("*"*60, end="\n")
  print(f"{bcolors.OKGREEN}Cleanup Done{bcolors.ENDC}")


def runProgram(labname):
  """
  Main program to run
  """
  testType = input("Test Type [rspec or bundle or npm or codechal]: ")
  phrase = input("Unique Phrase: ")

  if testType.strip() == "":
    print(f"{bcolors.WARNING}Make sure you enter test type \n{bcolors.ENDC}")
    runProgram(labname)
  elif testType.strip() == "bundle" or testType.strip() == "rspec" or testType.strip() == "npm" or testType.strip() == "codechal":
    # get my students
    myStudents = getMyStudents()
    if testType.strip() == "codechal":
      codeChallenges()
      print(f'{bcolors.OKGREEN}Done Unbundle{bcolors.ENDC}')
    else:
      createheader(labname)
      main(labname, testType, myStudents, phrase)
      cleanup(labname)
      print(f'{bcolors.OKGREEN}Done Marking{bcolors.ENDC}')
  else:
    print(f"{bcolors.WARNING}Make sure the spelling is correct \n{bcolors.ENDC}")
    runProgram(labname)



if __name__ == '__main__':
  try:
    if os.path.isfile('important_docs/myStudents.txt'):
      startTime = time.time() # in seconds
      labname = input("Lab Name [studentResults]: ") or "studentResults"
      runProgram(labname)

      timeTaken = strftime('%H:%M:%S', gmtime(time.time()-startTime))
      print(f"Marking Time: {timeTaken} minutes")
    else:
      print("*"*60)
      print(f"{bcolors.FAIL}Error: Make sure myStudents.txt file exists in 'important_docs' directory{bcolors.ENDC}")
      print("*"*60)

  except FileNotFoundError:
    print("*"*60)
    print(f"{bcolors.FAIL}Error: Make sure Submissions file exists in the root directory{bcolors.ENDC}")
