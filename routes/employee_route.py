from datetime import datetime
from exceptions import PermissionDenied
from daos.file_dao import FileDAO
from daos.request_dao import RequestDAO
from daos.user_dao import UserDAO
from entities.file import File
from entities.request import Request
from entities.user import User
from flask import Flask, request, jsonify, send_file
from services.employee import EmployeeService
import functools
import io
import json
import jwt

e = EmployeeService(FileDAO, RequestDAO, UserDAO)


def check_errors(func):
    @functools.wraps(func)
    def wrapper_check_errors(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return "Session expired; try logging in again.", 200
        except jwt.InvalidSignatureError:
            return "Token invalid.", 400
        except PermissionDenied:
            return "User lacks permissions.", 400
        except Exception as e:
            print(e)

    return wrapper_check_errors


def create_routes(app: Flask):
    @app.route("/employee/user", methods=["GET"])
    @check_errors
    def e_get_user():
        token = request.headers["token"]
        usr_id = User.decode_auth_token(token)
        return e.get_user(usr_id).to_json(), 200

    @app.route("/employee/request", methods=["GET"])
    @check_errors
    def e_get_requests_from_uid():
        token = request.headers["token"]
        usr_id = User.decode_auth_token(token)
        return jsonify([
            request.to_json() for request in e.get_requests_from_uid(usr_id)
        ]), 200

    @app.route("/employee/request", methods=["POST"])
    @check_errors
    def e_post_request():
        token = request.headers["token"]
        form = json.loads(request.data.decode("utf-8"))
        usr_id = User.decode_auth_token(token)
        req = Request(0, usr_id, float(form["amount"]))
        req.add_comment(usr_id, form["comment"])
        return e.create_request(req).to_json(), 200

    @app.route("/employee/request", methods=["PATCH"])
    @check_errors
    def e_update_request():
        token = request.headers["token"]
        form = json.loads(request.data.decode("utf-8"))
        usr_id = User.decode_auth_token(token)
        req_id = form["req_id"]
        req = e.get_user_specific_request(usr_id, req_id)
        req.request_amount = float(form["req_amount"])
        return e.edit_request(req).to_json(), 200

    @app.route("/employee/comment", methods=["GET"])
    @check_errors
    def e_read_comments():
        token = request.headers["token"]
        usr_id = User.decode_auth_token(token)
        req_id = request.headers["req_id"]
        req = e.get_user_specific_request(usr_id, req_id)
        return jsonify(e.read_comments(req)), 200

    @app.route("/employee/comment", methods=["POST"])
    @check_errors
    def e_add_comment():
        token = request.headers["token"]
        form = json.loads(request.data.decode("utf-8"))
        usr_id = User.decode_auth_token(token)
        req_id = int(form["req_id"])
        req = e.get_user_specific_request(usr_id, req_id)
        return e.add_comment(req, usr_id, form["comment"]).to_json(), 200

    @app.route("/employee/comment", methods=["PATCH"])
    @check_errors
    def e_edit_comment():
        token = request.headers["token"]
        form = json.loads(request.data.decode("utf-8"))
        usr_id = User.decode_auth_token(token)
        req_id = int(form["req_id"])
        req = e.get_user_specific_request(usr_id, req_id)
        return e.edit_comment(req, usr_id, int(form["index"]),
                              form["comment"]).to_json(), 200

    @app.route("/employee/file", methods=["POST"])
    @check_errors
    def e_post_image():
        token = request.headers["token"]
        usr_id = User.decode_auth_token(token)
        form = request.form
        req_id = int(form["req_id"])
        req = e.get_user_specific_request(usr_id, req_id)
        files = request.files.getlist("images")
        success = []
        for file in files:
            f_name = file.filename.rpartition(".")[0]
            f_ext = file.filename.rpartition(".")[2]
            upload = File(0, usr_id, req.id, f_name, f_ext, file.stream.read(),
                          datetime.now())
            e.attach_file(upload)
            success.append(str(upload))
        return "\n".join(success), 200

    @app.route("/employee/file", methods=["PATCH"])
    @check_errors
    def e_get_image_filenames():
        token = request.headers["token"]
        usr_id = User.decode_auth_token(token)
        form = request.form
        req_id = int(form["req_id"])
        req = e.get_user_specific_request(usr_id, req_id)
        return jsonify(e.get_filenames_from_request(req.id)), 200

    @app.route("/employee/file", methods=["GET"])
    @check_errors
    def e_get_image():
        token = request.headers["token"]
        usr_id = User.decode_auth_token(token)
        form = request.form
        fil_id = int(form["fil_id"])
        fil = e.get_user_specific_file(usr_id, fil_id)
        if fil.ext == "jpg":
            fil.ext = "jpeg"
        return send_file(io.BytesIO(fil.uploaded),
                         mimetype=f"image/{fil.ext}",
                         download_name=f"{fil.filename}.{fil.ext}"), 200
