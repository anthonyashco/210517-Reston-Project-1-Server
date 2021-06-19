from exceptions import SettingsNotFound
from flask import Flask
from flask_cors import CORS
from os.path import exists
from routes import employee_route, login_route, manager_route
import secrets
import yaml


def create_app():
    app = Flask(__name__, static_url_path="/static")

    if exists("settings.yml"):
        with open("settings.yml") as f:
            settings = yaml.safe_load(f)
        try:
            app.secret_key = settings["app"]["secret"]
        except KeyError:
            secret = secrets.token_hex(16)
            if "app" not in settings:
                settings["app"] = {}
            settings["app"]["secret"] = secret
            with open("settings.yml", "w") as f:
                yaml.safe_dump(settings, f)
            app.secret_key = secret
    else:
        raise SettingsNotFound

    CORS(app)
    employee_route.create_routes(app)
    login_route.create_routes(app)
    manager_route.create_routes(app)
    return app


app = create_app()
