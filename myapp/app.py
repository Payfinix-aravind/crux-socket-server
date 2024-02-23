from flask import Flask
from myapp.db import init_app
from myapp import settings
from blueprints.sockets.connections import socketio
from blueprints.api.client import  client_blueprint



def create_app():
    app = Flask(__name__)
    settings.init(app)
    init_app(app)
    app.register_blueprint(client_blueprint, url_prefix="/api")
    socketio.init_app(app,cors_allowed_origins="*")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()