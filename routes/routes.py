from flask import Flask, request, jsonify


def create_routes(app: Flask):

    @app.route("/")
    def hello():
        return "Hello world!", 200

    @app.route("/form", methods=["GET"])
    def test_form():
        return app.send_static_file("main.html"), 200

    @app.route("/form_input", methods=["POST"])
    def input_data():
        name = request.form["name"]
        starter = request.form["starter"]
        trainer = {"name": name, "starter": starter}
        return jsonify(trainer), 200
