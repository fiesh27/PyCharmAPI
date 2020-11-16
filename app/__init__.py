from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    db.init_app(app)
    migrate.init_app(app,db)

    from app.blueprints.users import bp as users
    app.register_blueprint(users)

    from app.blueprints.blog import bp as blog
    app.register_blueprint(blog)

    return app


from app import models



