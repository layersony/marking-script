import json
import codecs
import os
from bs4 import BeautifulSoup
import subprocess
import csv

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

def main(labname):
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
    gitlink = "/".join(gitSplit[:5]).split('?')[0]
    
    gitRepoName = gitSplit[4].split('.')[0].split('?')[0]
    print(studentUsername)

    # run system command
    subprocess.run(["mkdir", f"{studentUsername}"])

    if "fis-wip" in gitSplit or "commit" in gitSplit:
      status = "Incomplete"
      msg = "Push your Code to the Master Branch"
    else:
      if len(gitSplit) == 5 or "master" in gitSplit:
        # save test result in this.json file
        subprocess.run(f"cd {studentUsername}; git clone {gitlink}; cd {gitRepoName}; rspec -f j -o this.json", shell=True)
        
        pathThisJson = f"{os.getcwd()}/{studentUsername}/{gitRepoName}/this.json"

        with open(pathThisJson) as f:
          data = json.load(f)

        exampleCount = data['summary']['example_count'] # total number of examples
        failureCount = data['summary']['failure_count'] # failed number of examples

        if failureCount >= exampleCount/2:
          status = "Incomplete"
          msg = "Either Test Failed or Do Push your code"
        else:
          status = "Complete"

    # new instance
    newInstance(labname, sname, gitSplit[3], status, msg)
    subprocess.run(f"rm -rf {os.getcwd()}/{studentUsername}/", shell=True)
    print("="*60)

if __name__ == '__main__':
  labname = input("Lab Name: ")
  createheader(labname)
  main(labname)
  print('Done Marking')
