import os


class Config:
    SECRET_KEY = "super secret string"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance/dbgestionbudget.db')}"
