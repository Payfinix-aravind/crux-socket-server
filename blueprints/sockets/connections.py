from myapp.socket import socketio
from flask import request
from handler.sockethandler.handler import socket_intial_connection, leave_room_client, broadcast_liveloc, search_device

@socketio.on('LOCATION_TRACKING')
def getLocations(message):
    broadcast_liveloc(message, request.sid, request.headers)

@socketio.on('BATTERY_TRACKING')
def getBatteryTrack(message):
    print(message)

@socketio.on('SEARCH_DEVICE')
def searchDevice(message):
    search_device(message, request.sid, request.headers)

@socketio.on('connect')
def connect():
    socket_intial_connection(request.sid, request.headers)

@socketio.on('disconnect')
def disconnect():
    print("disconnect", request.sid)
    leave_room_client(request.headers)