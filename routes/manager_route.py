from datetime import datetime
from exceptions import PermissionDenied
from daos.file_dao import FileDAO
from daos.request_dao import RequestDAO
from daos.user_dao import UserDAO
from entities.user import User
from flask import Flask, request, jsonify, send_file
from services.manager import ManagerService
import functools
import io
import json
import jwt

m = ManagerService(FileDAO, RequestDAO, UserDAO)


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


def is_manager(token) -> User:
    usr_id = User.decode_auth_token(token)
    usr = m.get_user(usr_id)
    if usr.status != "manager":
        raise PermissionDenied
    return usr


def create_routes(app: Flask):
    @app.route("/manager/user", methods=["GET"])
    @check_errors
    def m_get_user():
        token = request.headers["token"]
        usr_id = User.decode_auth_token(token)
        return m.get_user(usr_id).to_json(), 200

    @app.route("/manager/request", methods=["GET"])
    @check_errors
    def m_get_requests():
        is_manager(request.headers["token"])
        return jsonify([request.to_json()
                        for request in m.get_requests()]), 200

    @app.route("/manager/request/pending", methods=["GET"])
    @check_errors
    def m_get_pending():
        is_manager(request.headers["token"])
        return jsonify([request.to_json() for request in m.get_pending()]), 200

    @app.route("/manager/request/completed", methods=["GET"])
    @check_errors
    def m_get_completed():
        is_manager(request.headers["token"])
        return jsonify([request.to_json()
                        for request in m.get_completed()]), 200

    @app.route("/manager/request", methods=["PATCH"])
    @check_errors
    def m_update_request():
        is_manager(request.headers["token"])
        form = json.loads(request.data.decode("utf-8"))
        req_id = form["req_id"]
        req = m.get_request(req_id)
        req.request_amount = float(form["req_amount"])
        return m.edit_request(req).to_json(), 200

    @app.route("/manager/comment", methods=["GET"])
    @check_errors
    def m_read_comments():
        req = request.headers("req_id")
        return jsonify(m.read_comments(req)), 200

    @app.route("/manager/comment", methods=["POST"])
    @check_errors
    def m_add_comment():
        usr = is_manager(request.headers["token"])
        form = json.loads(request.data.decode("utf-8"))
        req_id = int(form["req_id"])
        req = m.get_request(req_id)
        return m.add_comment(req, usr.id, form["comment"]).to_json(), 200

    @app.route("/manager/comment", methods=["PATCH"])
    @check_errors
    def m_edit_comment():
        usr = is_manager(request.headers["token"])
        form = json.loads(request.data.decode("utf-8"))
        req_id = int(form["req_id"])
        index = int(form["index"])
        req = m.get_request(req_id)
        return m.edit_comment(req, usr.id, index,
                              form["comment"]).to_json(), 200

    @app.route("/manager/file", methods=["PATCH"])
    @check_errors
    def m_get_image_filenames():
        is_manager(request.headers["token"])
        form = json.loads(request.data.decode("utf-8"))
        req_id = int(form["req_id"])
        req = m.get_request(req_id)
        return jsonify(m.get_filenames_from_request(req.id)), 200

    @app.route("/manager/file", methods=["GET"])
    @check_errors
    def m_get_image():
        is_manager(request.headers["token"])
        form = json.loads(request.data.decode("utf-8"))
        fil_id = int(form["fil_id"])
        fil = m.get_file(fil_id)
        if fil.ext == "jpg":
            fil.ext = "jpeg"
        return send_file(io.BytesIO(fil.uploaded),
                         mimetype=f"image/{fil.ext}",
                         download_name=f"{fil.filename}.{fil.ext}"), 200

    @app.route("/manager/approve", methods=["POST"])
    @check_errors
    def m_decision():
        usr = is_manager(request.headers["token"])
        form = json.loads(request.data.decode("utf-8"))
        req = m.get_request(form["req_id"])
        if form["decision"] == "approve":
            req.decision = True
        elif form["decision"] == "deny":
            req.decision = False
        else:
            raise ValueError
        req.decision_time = datetime.now()
        req.manager_id = usr.id
        return m.update_request(req).to_json(), 200
