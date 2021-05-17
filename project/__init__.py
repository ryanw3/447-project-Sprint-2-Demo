from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#import secrets_ignore
# init SQLAlchemy so we can use it later in our models
import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path) 

db = SQLAlchemy()



def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'jrgeaoiro9p032qujpraWKGV403Q42GJWMW390Pnhgw432'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    db.init_app(app)
    return app
