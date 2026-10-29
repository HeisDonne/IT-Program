from flask import Flask

from app.config import Config
from app.extensions import bcrypt, db, jwt, mail, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)

    return app