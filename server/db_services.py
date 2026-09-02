def saveAction(action):
    print('action saved')

def getLastResolvedActionId(agent_id):
    return 1

def generateAgentId(hostName):
    return int(input(f'give a new agent id for {hostName}: '))

def fetchExtensions(agent_id):
    return ['.txt','.py']


def fetchRoots(agent_id):
    return ['test_folder/']


def fetchPeriod(agent_id):
    return 1800