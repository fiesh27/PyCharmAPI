from app import db
from app.blueprints.blog import bp as blog
from flask import jsonify, request, url_for
from app.models import Blog, User


@blog.route('/', methods=['GET'])
def index():
    """
    [GET]   /blog/
    """
    data = {
        'blog': [i.to_dict() for i in Blog.query.all()]
    }
    return jsonify(data)


@blog.route('/<id>', methods=['GET'])
def get_blog(id):
    """
    [GET]   /blog/
    """
    i = Blog.query.get(id)
    data = {
        'blog': i.to_dict() if i else {}
    }
    return jsonify(data)


@blog.route('/', methods=['POST'])
def create_blog():
    """
    [POST] /blog/
    """
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = data.get('user_id')
    i = Blog(title, content, user_id)
    db.session.add(i)
    db.session.commit()
    response = jsonify(i.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('blog.get_blog', id=i.id)
    return response


@blog.route('/<int:id>', methods=['DELETE'])
def delete_blog(id):
    """
    [DELETE] /blog/<id>
    """
    post = Blog.query.get(id)
    if not post:
        return jsonify({"detail": f"Blog post with id:{id} does not exist"}), 400
    db.session.delete(post)
    db.session.commit()
    return jsonify({"detail": f"Blog post-{post.title} has been deleted"}), 201


@blog.route('/<int:id>', methods=['PUT'])
def update_blog(id):

    """
     [PUT] /blog/<id>
    """
    post = Blog.query.get(id)
    data = request.get_json()
    post.from_dict(data)
    db.session.commit()
    return jsonify({'blog': post.to_dict()}), 200