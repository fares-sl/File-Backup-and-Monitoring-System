from database.engine import SessionLocal
from database.models.actions import Action 
from database.models.Agent import Agent
import config

def saveAction(action, agent_id):
    with SessionLocal() as session:
        db_action = Action(
            id=action.id,
            agent_id=agent_id,
            path=action.path,
            action=action.action.value,
            user=action.user,
            action_time=action.time,
            old_path=action.oldPath
        )
        session.add(db_action)
        agent = session.get(Agent, agent_id)
        agent.last_resolved_action_id = action.id
        session.commit()
        print('action saved')

def getLastResolvedActionId(agent_id):
    with SessionLocal() as session:
        agent = session.get(Agent, agent_id)
        return agent.last_resolved_action_id

def generateAgentId(hostName):
    with SessionLocal() as session:
        agent = Agent(
            hostname = hostName,
            watched_roots = config.DEFAULT_ROOTS,
            watched_extensions = config.DEFAULT_EXTENSIONS,
            period = config.DEFAULT_PERIOD
        )
        session.add(agent)
        session.commit()
        return agent.agent_id
    

def fetchExtensions(agent_id):
    with SessionLocal() as session:
        agent = session.get(Agent, agent_id)
        return agent.watched_extensions


def fetchRoots(agent_id):
    with SessionLocal() as session:
        agent = session.get(Agent, agent_id)
        return agent.watched_roots

def fetchPeriod(agent_id):
    with SessionLocal() as session:
        agent = session.get(Agent, agent_id)
        return agent.period