from flask_socketio import emit
from myapp.db import db
from sqlalchemy import text
import json


def configuration_type(distrbution_data, type):
    return {
        'enabled': distrbution_data[type]['geo_tracking'],
        'history_enabled': distrbution_data[type]['history_enabled'],
        'range':  distrbution_data[type]['range']
    }


def emit_to_devices(distrbution_data,type):

    condition = 'and enterprise_id in :enterprises_list' if not distrbution_data[type]['track_all'] else ''
    condition += f" and type = '{'Fully Managed' if type=='dedicated_dev' else 'Work Profile'}'"

    query = f"""
            select device_id, socket_id from enroll_devices where socket_id!='' {condition}
        """
    result = db.session.execute(text(query),{"enterprises_list": tuple(distrbution_data[type]['enterprises_list'])}).fetchall()

    data = {
            "org_id":distrbution_data['org_id'],
            "enterprise_id":distrbution_data['enterprise_id'],
            "type":"GEO_TRACKING",
            "configuration":configuration_type(distrbution_data, type),
            "status":True,
    }

    for item in result:
        print(item)
        emit('NEW_SETTING_CHANGE', json.dumps(data), to=item[1], namespace='/')


def emit_loc_settings(distrbution_data):
    emit_to_devices(distrbution_data, 'dedicated_dev')
    emit_to_devices(distrbution_data, 'work_profile')
    return {
        "status":True,
        "message":"location settings updated"
    }
