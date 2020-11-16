from app import db
from app.blueprints.users import bp as users
from flask import jsonify, request, url_for
from app.models import User


@users.route('/', methods=['GET'])
def index():
    """
    [GET]   /users/
    """
    data = {
        'users': [user.to_dict() for user in User.query.all()]
    }
    return jsonify(data)


@users.route('/<email>', methods=['GET'])
def get_user(email):
    """
    [GET]   /users/
    """
    user = User.query.filter_by(email=email).first()
    data = {
        'users': user.to_dict() if user else {}
    }
    return jsonify(data)


@users.route('/', methods=['POST'])
def create_user():
    """
    [POST] /users/
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User(email, password)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('users.get_user', email=user.email)
    return response


@users.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    """
    [DELETE] /users/<id>
    """
    user = User.query.get(id)
    if not user:
        return jsonify({"detail": f"User with id:{id} does not exist"}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({"detail": f"User-{user.email} has been deleted"}), 201


@users.route('/<int:id>', methods=['PUT'])
def update_user(id):

    """
     [PUT] /users/<id>
    """
    user = User.query.get(id)
    data = request.get_json()
    user.from_dict(data)
    db.session.commit()
    return jsonify({'users': user.to_dict()}), 200


