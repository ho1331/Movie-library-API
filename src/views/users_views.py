from app import db
from flask import Blueprint, request
from models.users import User

user = Blueprint("user", __name__)


@user.route("/users/check")
def ch():
    return "hello"


@user.route("/users", methods=["POST", "GET"])
def insert_user():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            new_user = User(
                name=data["name"],
                nick_name=data["nick_name"],
                email=data["email"],
                pswhash=data["pswhash"],
            )
            db.session.add(new_user)
            db.session.commit()
            return {
                "message": f"User {new_user.nick_name} has been created successfully."
            }
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == "GET":
        users = User.query.all()
        results = [
            {
                "id": user.id,
                "name": user.name,
                "nick_name": user.nick_name,
                "email": user.email,
                "pswhash": user.pswhash,
                "created": user.created,
            }
            for user in users
        ]

        return {"count": len(results), "users": results}
