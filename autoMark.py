#! /usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os, csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def login(email, passcode):
  driver.get('https://moringa.instructure.com/login')
  driver.find_element("id", "identifierId").send_keys(email)
  driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button').send_keys(Keys.RETURN)
  time.sleep(2)
  driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(passcode)
  driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button').send_keys(Keys.RETURN)

  time.sleep(50)
  print('Logged In SuccessFully...')

def getStudent(assign_id, filename):
  with open(f'markedCsv/{filename}.csv' , 'r') as csvfile:
      # create the object of csv.reader()
      csv_file_reader = csv.reader(csvfile,delimiter=',')
      for row in csv_file_reader:
          if row[0].isdigit():
            get_pages(assign_id, row[0], row[3], row[4])

def get_pages(assign_id, st_id, status, comment): 
  driver.get(f'https://moringa.instructure.com/courses/186/gradebook/speed_grader?assignment_id={assign_id}&student_id={st_id}')
  time.sleep(10)
  # for dropdown
  h = Select(driver.find_element('id', 'grading-box-extended'))
  if status == 'Complete':
    h.select_by_visible_text('Complete')
    h.select_by_value('complete')
  elif status == 'Incomplete':
    h.select_by_visible_text('Incomplete')
    h.select_by_value('incomplete')

  # text box comment
  driver.find_element('id','speed_grader_comment_textarea').send_keys(comment)
  driver.find_element(By.XPATH, '//*[@id="comment_submit_button"]').send_keys(Keys.RETURN)
  time.sleep(7)

if __name__ == '__main__':
  try:
    print('********** Moringa User Detail **********')
    email = input('Moringa Email [samuel.maingi@moringaschool.com]: ') or 'samuel.maingi@moringaschool.com'
    passcode = input('Moringa Passcode: ') or 'Madcity9586'
    assign_id = input('Assignment ID: ')
    filename = input('Marked Csv name: ')

    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.implicitly_wait(0.5)
    print('\n')
    login(email, passcode)
    time.sleep(5)
    getStudent(assign_id, filename)

    driver.close()
  except:
    print('\n\nUser Cancelled..')
