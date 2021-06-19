from utils.app import app
import yaml

with open("settings.yml") as f:
    settings = yaml.safe_load(f)


def test_app_config():
    assert app.config["SECRET_KEY"] == settings["app"]["secret"]
