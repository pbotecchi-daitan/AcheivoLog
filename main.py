from classes.SeleniumConnection import Selenium
from classes.Logging import Logging
import os
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('week', help='Digite o número da semana', type=int)

args = parser.parse_args()

def main():
  log = Logging()
  log.info("Starting LogHours bot")

  start = Selenium(os.environ["BROWSER"])
  start.startScript()

  log.info("Script completed successfully")

if __name__ == '__main__':
  main()