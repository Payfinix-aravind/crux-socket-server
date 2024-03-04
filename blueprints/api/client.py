from flask import jsonify, request,Blueprint, redirect
from handler.clienthandler.handler import emit_loc_settings, emit_battery_settings
import boto3

client_blueprint = Blueprint("client_blueprint", __name__)


@client_blueprint.route("/emitgeosettings", methods=["POST"])
def handle_geosettings():
    response = emit_loc_settings(request.json)
    return jsonify(response)

@client_blueprint.route("/emitbatsettings", methods=["POST"])
def handle_batterysettings():
    response = emit_battery_settings(request.json)
    return jsonify(response)


