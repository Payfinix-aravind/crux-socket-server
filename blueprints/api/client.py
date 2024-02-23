from flask import jsonify, request,Blueprint
from handler.clienthandler.handler import emit_loc_settings

client_blueprint = Blueprint("client_blueprint", __name__)


@client_blueprint.route("/emitgeosettings", methods=["POST"])
def handle_geosettings():
    response = emit_loc_settings(request.json)
    return jsonify(response)

@client_blueprint.route("/emitbatsettings", methods=["POST"])
def handle_batterysettings():
    response = emit_loc_settings(request.json)
    return jsonify(response)
