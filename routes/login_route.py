from daos.user_dao import UserDAO
from flask import Flask, render_template, request
from services.login import LoginService

l = LoginService(UserDAO)  # noqa: E741


def create_routes(app: Flask):

    @app.route("/")
    def hello():
        return render_template("index.html"), 200

    @app.route("/login", methods=["POST"])
    def login() -> str:
        body = request.form
        return l.login(body["email"], body["password"]), 200
