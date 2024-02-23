from flask_socketio import join_room, emit, leave_room
from myapp.db import db
from sqlalchemy import text
import json
from datetime import datetime


def dictfetchall(cursor):
    columns = [col for col in cursor.keys()]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def create_tracking_dict(trackingJson, type):
    condition = 'copown' if type=='fully managed' else 'byod'
    return {
            "enabled": trackingJson['GeoTracking']['tracking'] and  trackingJson['GeoTracking'][condition],
            "history_enabled":trackingJson['LocHistory']['tracking'] and trackingJson['LocHistory'][condition],
            "range":trackingJson['LocHistory']['range']
    }


def socket_intial_connection(socket_id, auth_info):
    client_type = auth_info.get('clientType', None)
    org_id = auth_info.get('orgId', "DUMMY") if client_type == 'LIVETRACKER' else ""
    print(client_type, org_id)

    if(client_type=='LIVETRACKER'):
        join_room(org_id)
    else:
        device_id = auth_info.get('deviceId')

        update_query = """update enroll_devices set socket_id = :socket_id where device_id = :device_id"""
        db.session.execute( text(update_query), {"device_id": device_id, "socket_id":socket_id})
        db.session.commit()
    
        query = f"""
                select 
                    u.org_id, u.enterprise_id, u.geo_tracking, e.device_id, e.type
                from uemsettings u join enroll_devices e
                on e.enterprise_id = u.enterprise_id where e.device_id = :device_id limit 1
            """
        
        result = db.session.execute(text(query),{"device_id": device_id}).fetchone()

        settings = {
            "geo_tracking": False,
            "history_enabled":False,
            "range":100
        }
        if result is not None and result[4] in ('Fully Managed', 'Work Profile'):
            settings = create_tracking_dict(result[2], result[4].lower())

        data = {
            "org_id": result[0] if result else "",
            "enterprise_id": result[1] if result else "",
            "location_tracking_configuration": settings,
            "status": bool(result)
        }
        emit('INITIAL', json.dumps(data))

def leave_room_client(auth_info):
    if(auth_info.get('clientType', None)=='LIVETRACKER'):
        leave_room(auth_info.get('orgId', "DUMMY"))


def broadcast_liveloc(message, socket_id, auth_info):
    print(message)
    message = json.loads(message)
    if(message['history']):
        print("history")
        get_location_query ="""
            select tracking_id, location_data from location_history 
            where enterprise_id=:enterprise_id and device_id=:device_id and DATE(created_at) = :date 
        """
        result = db.session.execute(
            text(get_location_query),{
                "device_id": message['device_id'], 
                "enterprise_id":message['enterprise_id'],
                "date": datetime.now().strftime('%Y-%m-%d')
            }).fetchone()
        if(result):
            update_query = """update location_history set location_data = :location_data, updated_at =:updated_at where tracking_id = :tracking_id"""
            location_data =result[1]
            location_data.append({"location":message['location'], "timeStamp":message["timeStamp"]})
            result = db.session.execute(
                text(update_query),{
                    "location_data": json.dumps(location_data), 
                    "tracking_id":result[0],
                    "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            db.session.commit()
        else:
            insert_query = """ insert into location_history (device_id, enterprise_id, type, platformos, created_at, updated_at, location_data) 
                values (:device_id, :enterprise_id, :type, :platformos, :created_at, :updated_at, :location_data)"""
            
            db.session.execute(
                text(insert_query), 
                {
                    "device_id": message['device_id'], 
                    "enterprise_id":message['enterprise_id'], 
                    "type":"Fully Managed",
                    "platformos":"android", 
                    "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                    "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                    "location_data":json.dumps([{"location":message['location'], "timeStamp":message["timeStamp"]}])
                })
            db.session.commit()
    
    emit('LOCATION_TRACKING_UI', message, room=message.get('device_id', "DUMMY"))


    