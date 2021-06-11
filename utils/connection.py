from psycopg2 import connect
import yaml


class Connection():
    with open("settings.yml", "r") as f:
        settings = yaml.safe_load(f)
        postgres = settings["postgres"]
    conn = connect(**postgres[postgres["type"]])
