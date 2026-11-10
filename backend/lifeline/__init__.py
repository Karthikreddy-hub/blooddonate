from flask import Flask
from flask_wtf.csrf import CSRFProtect

from .config import Config
from .extensions import db, login_manager

csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .models import User
    from .routes import main

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    app.register_blueprint(main)

    @app.cli.command("init-db")
    def init_db():
        """Create tables that do not exist yet."""
        db.create_all()
        print("Database tables are ready.")

    return app
