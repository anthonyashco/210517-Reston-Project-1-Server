"""Main program script."""

import logging

from flask import Flask
from routes import routes

app = Flask(__name__, static_url_path="/static")
logging.basicConfig(
    filename="log.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
routes.create_routes(app)

if __name__ == "__main__":
    app.run()
