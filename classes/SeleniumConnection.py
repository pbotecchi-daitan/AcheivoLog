from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.support.ui import Select
import random
import time
import os

from classes.DateHandler import DateHandler
from classes.Logging import Logging

from dotenv import load_dotenv
load_dotenv()

class Selenium(Logging):
  def __init__(self, browser):
    super().__init__()
    self.browser = browser
    self.delay = 15
    self.service = None
    self.navigator = None
    self.setService()

  def setService(self):
    if (self.browser == 'firefox'):
      self.service = Service(GeckoDriverManager().install())
      self.navigator = webdriver.Firefox(service=self.service)
    else :
      self.service = ChromeService(ChromeDriverManager().install())
      self.navigator = webdriver.Chrome(service=self.service)

  def getService(self):
    return self.service
  
  def getNavigator(self):
    return self.navigator

  def fillDays(self, days, dateHandler, navigator):
    navigator.switch_to.frame('main')

    for day in days:
      WebDriverWait(navigator, self.delay).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="diai"]')))
      navigator.find_element('xpath', '//*[@id="diai"]').click()
      select_day = Select(navigator.find_element('xpath', '//*[@id="diai"]'))
      select_day.select_by_value(str(day))

      select_entry_hour = Select(navigator.find_element('xpath', '//*[@id="timehH"]'))
      select_entry_hour.select_by_value(dateHandler.getEntryHour())

      select_entry_minute = Select(navigator.find_element('xpath', '//*[@id="timemH"]'))
      select_entry_minute.select_by_index(str(random.randint(0, 37)))

      WebDriverWait(navigator, self.delay).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/form/div[13]/input')))
      navigator.find_element('xpath', '/html/body/div[1]/div/div[1]/form/div[13]/input').click()

      time.sleep(1)

      navigator.find_element('xpath', '//*[@id="startBreak6"]').send_keys(str(dateHandler.getLunchBreak()))
      lunch_break_minute = random.randint(0, 15)
      navigator.find_element('xpath', '//*[@id="startBreak6"]').send_keys(str(lunch_break_minute))
      lunch_break_increase = random.randint(30, 45)

      navigator.find_element('xpath', '//*[@id="endBreak6"]').send_keys(str(dateHandler.getLunchBreak()))
      navigator.find_element('xpath', '//*[@id="endBreak6"]').send_keys(str(lunch_break_minute  + lunch_break_increase))

      WebDriverWait(navigator, self.delay).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/form/input')))
      navigator.find_element('xpath', '/html/body/div[1]/div/div[2]/div[2]/form/input').click()

      time.sleep(1)

  def signIn(self, navigator):
    WebDriverWait(navigator, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0116"]')))
    navigator.find_element('xpath', '//*[@id="i0116"]').send_keys(os.environ["EMAIL"])
    navigator.find_element('xpath', '//*[@id="idSIButton9"]').click()

    time.sleep(1)

    WebDriverWait(navigator, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0118"]')))
    navigator.find_element('xpath', '//*[@id="i0118"]').send_keys(os.environ["PASSWORD"])
    WebDriverWait(navigator, self.delay).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Sign in']")))

    time.sleep(1)
    navigator.find_element('xpath', "//input[@value='Sign in']").click()

    WebDriverWait(navigator, self.delay).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idChkBx_SAOTCAS_TD"]')))
    navigator.find_element('xpath', '//*[@id="idChkBx_SAOTCAS_TD"]').click()
    
    WebDriverWait(navigator, 50).until(EC.url_changes('https://login.microsoftonline.com/common/SAS/ProcessAuth'))

    WebDriverWait(navigator, self.delay).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="KmsiCheckboxField"]')))
    navigator.find_element('xpath', '//*[@id="KmsiCheckboxField"]').click()

    self.info('Allow the access using your phone')

    WebDriverWait(navigator, self.delay).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Yes']")))
    navigator.find_element('xpath', "//input[@value='Yes']").click()

  def startScript(self):
    navigator = self.getNavigator()
    navigator.get(os.environ["URL_PATH"])
    dateHandler = DateHandler()

    try:
      self.info('Starting Login process, make sure you are conneted inside the vpn')
      self.signIn(navigator)
      self.info('Log in occured successfuly. Start logging hours')
      days = dateHandler.getDaysOfTheWeek()
      self.fillDays(days, dateHandler, navigator)
      self.info('Hours logged succesfuly. Ending Script')

    except TimeoutException:
          self.info('An Error occured during the process!')
