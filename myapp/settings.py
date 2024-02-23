from flask import Flask
from myapp.config import ApplicationConfig

def init(app:Flask):
    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=ApplicationConfig.DB_TRACK_MODIFICATIONS,
        SQLALCHEMY_DATABASE_URI=ApplicationConfig.DATABASE_URI,
    )