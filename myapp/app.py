from flask import Flask
from flask_cors import CORS
from myapp.db import init_app
from myapp import settings
from blueprints.sockets.connections import socketio
from blueprints.api.client import  client_blueprint
from blueprints.api.trueread import trueread_blueprint



def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    settings.init(app)
    init_app(app)
    app.register_blueprint(client_blueprint, url_prefix="/api")
    app.register_blueprint(trueread_blueprint, url_prefix="/trueread")
    socketio.init_app(app,cors_allowed_origins="*", websocket=True)
    return app

if __name__ == '__main__':
    app = create_app()
    # app.run()
    socketio.run()