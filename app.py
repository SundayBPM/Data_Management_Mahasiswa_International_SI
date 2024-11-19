# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import secrets


db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.secret_key = secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_mahasiswa.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # app.config['SESSION_PERMANENT'] = False
    # app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    # app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    # app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    # app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    # app.config['MAIL_USE_TLS'] = False
    # app.config['MAIL_USE_SSL'] = True

    #Take the secret key from .env file
    # app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    db.init_app(app)

    from routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)

    return app
