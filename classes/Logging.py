import logging

class Logging():
  def __init__(self):
    self.setup_logging()

  def setup_logging(self):
    logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s %(levelname)s:%(message)s'
    )

  def info(self, message):
    logging.info(message)