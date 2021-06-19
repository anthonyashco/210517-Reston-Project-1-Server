"""Main program script."""

import logging
from utils.app import app

logging.basicConfig(
    filename="log.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

if __name__ == "__main__":
    app.run()
