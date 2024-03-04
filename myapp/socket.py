from flask_socketio import SocketIO

socketio = SocketIO(logger=False, engineio_logger=False, cors_allowed_origin="*")