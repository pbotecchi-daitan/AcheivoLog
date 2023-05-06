import os
from datetime import datetime
from datetime import timedelta
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("week", help="desired week you wanna fill", type=int)
args = parser.parse_args()

class DateHandler:
  def __init__(self):
    self.entry_hour = os.environ["ENTRY_HOUR"]
    self.lunch_break = os.environ["LUNCH_BREAK"]

  def getEntryHour(self):
    return self.entry_hour

  def getLunchBreak(self):
    return self.lunch_break

  def getDaysOfTheWeek(self):
    dayOfWeek = f"2023-W{int(args.week)}"
    startDay = datetime.strptime(dayOfWeek + '-1', "%Y-W%W-%w")

    dayArray = [startDay.day]

    for i in range(4):
      nextDay = startDay + timedelta(days=(i + 1))
      dayArray.append(nextDay.day)

    return dayArray