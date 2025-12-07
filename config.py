import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "super-secret-key"
    # ?SQLALCHEMY_DATABASE_URI = "sqlite:///instance/app.db"
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///instance/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
