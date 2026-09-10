from database.engine import SessionLocal
from database.models.actions import Action 
from database.models.device import Device
from database.models.User import User
import config

def saveAction(action, device_id):
    with SessionLocal() as session:
        db_action = Action(
            id=action.id,
            device_id=device_id,
            path=action.path,
            action=action.action.value,
            user=action.user,
            action_time=action.time,
            old_path=action.oldPath
        )
        session.add(db_action)
        user = session.get(User, (device_id, action.user))
        user.last_resolved_action_id = action.id
        session.commit()
        print('action saved')

def getLastResolvedActionId(device_id, user):
    with SessionLocal() as session:
        user_db = session.get(User, (device_id,user))
        return user_db.last_resolved_action_id


def generateDeviceId(hostName, platform, mac):
    with SessionLocal() as session:
        device = Device(
            hostname = hostName,
            platform = platform,
            mac = mac
        )
        session.add(device)
        session.commit()
        return device.device_id

def registerUser(device_id, user, watched_roots, watched_extensions, period):
    with SessionLocal() as session:
        user_db = session.get(User, (device_id, user))
        if user_db is None:
            user_db = User(
                device_id = device_id,
                user = user,
                watched_roots = watched_roots,
                watched_extensions = watched_extensions,
                period = period
            )
            session.add(user_db)
            session.commit()

    

def fetchExtensions(device_id, user):
    with SessionLocal() as session:
        user_db = session.get(User, (device_id, user))
        return user_db.watched_extensions


def fetchRoots(device_id, user):
    with SessionLocal() as session:
        user_db = session.get(User, (device_id, user))
        return user_db.watched_roots

def fetchPeriod(device_id, user):
    with SessionLocal() as session:
        user_db = session.get(User, (device_id, user))
        return user_db.period