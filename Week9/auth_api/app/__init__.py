from flask import Flask, jsonify

from app.config import Config
from app.extensions import bcrypt, db, jwt, mail, migrate
from werkzeug.exceptions import HTTPException
from app.logging_config import setup_logging
import os
from flask import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint


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

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        return jsonify({"error": e.name, "message": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        app.logger.exception("Unhandled error")
        return jsonify({"error": "Internal Server Error"}), 500

    setup_logging(app)

    if os.environ.get("ENABLE_DOCS", "false").lower() == "true":
        docs_dir = os.path.join(os.path.dirname(__file__), "docs")

        @app.route("/openapi.yaml")
        def openapi_spec():
            return send_from_directory(docs_dir, "openapi.yaml")

        app.register_blueprint(
            get_swaggerui_blueprint("/docs", "/openapi.yaml", config={"app_name": "Authentication API"})
        )

    return app
