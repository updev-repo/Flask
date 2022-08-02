from flask import Blueprint, jsonify

from apps.auth.model.user import User

api = Blueprint("api", __name__, url_prefix="/api", template_folder="./templates")


@api.route("/users")
def all_users():
    users = User.query.all()
    return jsonify(users)
