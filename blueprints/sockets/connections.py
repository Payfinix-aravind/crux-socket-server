from myapp.socket import socketio
from flask import request
from handler.sockethandler.handler import socket_intial_connection, leave_room_client, broadcast_liveloc

@socketio.on('LOCATION_TRACKING')
def getLocations(message):
    broadcast_liveloc(message, request.sid, request.headers)

@socketio.on('BATTERY_TRACKING')
def getBatteryTrack(message):
    print(message)

@socketio.on('connect')
def connect():
    print("connect", request.sid)
    socket_intial_connection(request.sid, request.headers)

@socketio.on('disconnect')
def disconnect():
    print("disconnect", request.sid)
    leave_room_client(request.headers)