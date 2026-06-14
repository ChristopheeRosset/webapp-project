from pathlib import Path
from flask import Flask
from .models import db
import server.config as config

config_values = config.load_config()


def create_app():
    app = Flask(__name__)
    app.secret_key = config_values["BACKEND"]["SECRET_KEY"]
    base_dir = Path(__file__).resolve().parent
    db_path = base_dir / "db" / config_values["DB"]["DB_NAME"]
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    db.init_app(app)

    from .auth import auth
    from .views import views
    
    app.register_blueprint(auth)
    app.register_blueprint(views)

    from .models import User

    with app.app_context():
        db.create_all()

    return app
