from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "views.login_view"

    with app.app_context():
        from src import models
        from src.controllers import views_bp

        app.register_blueprint(views_bp)

        db.create_all()

    return app
