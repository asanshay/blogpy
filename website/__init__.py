from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = "somethign"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
    app.config['UPLOAD_FOLDER'] = "assests/user_profile_picture"

    from .view import view
    from .auth import auth
    from .models import Author, Blog
    
    app.register_blueprint(view)
    app.register_blueprint(auth)


    db.init_app(app)
    login_manager.init_app(app)
    

    login_manager.login_view = "auth.login"

    with app.app_context():
        db.create_all()

    return app
