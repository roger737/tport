import os
import logging
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(test_config: dict | None = None) -> Flask:
    """Application factory.

    The application is configured to use SQLite by default so it can run
    fully offline.  A ``DATABASE_URL`` environment variable may be supplied
    to use a different backend such as PostgreSQL.
    """
    app = Flask(__name__, instance_relative_config=True)
    upload_dir = Path(app.instance_path) / 'uploads'
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///audit.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=str(upload_dir),
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    # Ensure instance folders exist for uploads and logging
    upload_dir.mkdir(parents=True, exist_ok=True)
    log_file = Path(app.instance_path) / 'audit.log'
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )

    # Import and register blueprints lazily to avoid circular imports
    from .auth import auth_bp
    from .audits import audit_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(audit_bp)

    @app.route('/')
    def index():
        from flask_login import current_user
        if current_user.is_authenticated:
            return "Welcome {}".format(current_user.username)
        return "Welcome to the Audit Tool"

    return app
