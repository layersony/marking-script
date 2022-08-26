import json
import codecs
import os
from bs4 import BeautifulSoup
import subprocess
import csv
import time
from time import gmtime, strftime


class bcolors:
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'

def newInstance(labname, name, gitname, status, msg):
  data = [name, gitname, status, msg]
  with open(f'{labname}.csv', 'a', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data)


def createheader(labname):
  header = ['Student Name', 'Git Name', 'Status', 'Message']
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
  subprocess.run(f"cd {params.get('studentUsername')}; git clone {params.get('gitlink')}; cd {params.get('gitRepoName')}; bundle config set --local path 'vendor/bundle'; bundle install --retry=2; learn test -o this; cp .results.json this.json", shell=True)
  pathThisJson = f"{os.getcwd()}/{params.get('studentUsername')}/{params.get('gitRepoName')}/this.json"
  return pathThisJson


def main(labname, testType):
  for filename in os.listdir(f"{os.getcwd()}/submissions"):

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

    gitSplit = glink.split('/')
    studentUsername = gitSplit[3]
    gitlink = "/".join(gitSplit[:5]).split('?')[0].split('#')[0]

    gitRepoName = gitSplit[4].split('.')[0].split('?')[0].split('#')[0]
    print(studentUsername)

    # creates folder for student
    subprocess.run(["mkdir", f"{studentUsername}"])

    if "fis-wip" in gitSplit or "commit" in gitSplit or "fis-whip" in gitSplit:
      status = "Incomplete"
      msg = "Push your Code to the Master Branch"
    else:
      if len(gitSplit) == 5 or "master" in gitSplit or "main" in gitSplit:
        params = {
            "studentUsername": studentUsername,
            "gitlink": gitlink,
            "gitRepoName": gitRepoName
        }
        # marking starts
        if testType.lower() == 'rspec':
          filepath = rspecMark(params)
        else:
          filepath = bundleMark(params)

        with open(filepath) as f:
          data = json.load(f)

          # total number of examples
          exampleCount = data['summary']['example_count']
          # failed number of examples
          failureCount = data['summary']['failure_count']

          if failureCount >= exampleCount/2:
            status = "Incomplete"
            msg = "Either Test Failed or Do Push your code"
          else:
            status = "Complete"
            msg = "Good Work"

    # new instance
    newInstance(labname, sname, gitSplit[3], status, msg)
    subprocess.run(f"rm -rf {os.getcwd()}/{studentUsername}/", shell=True)
    print("="*60)


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
  testType = input("Test Type [rspec or bundle]: ")

  if testType.strip() == "":
    print(f"{bcolors.WARNING}Make sure you enter test type \n{bcolors.ENDC}")
    runProgram(labname)
  elif testType.strip() == "bundle" or testType.strip() == "rspec":
    createheader(labname)
    main(labname, testType)
    print(f'{bcolors.OKGREEN}Done Marking{bcolors.ENDC}')
    cleanup(labname)
  else:
    print(f"{bcolors.WARNING}Make sure the spelling is correct \n{bcolors.ENDC}")
    runProgram(labname)



if __name__ == '__main__':
  try:
    startTime = time.time() # in seconds
    labname = input("Lab Name [studentResults]: ") or "studentResults"
    runProgram(labname)

    timeTaken = strftime('%H:%M:%S', gmtime(time.time()-startTime))
    print(f"Marking Time: {timeTaken} minutes")

  except FileNotFoundError:
    print("*"*60)
    print(f"{bcolors.FAIL}Error: Make sure Submissions file exists in the root directory{bcolors.ENDC}")
