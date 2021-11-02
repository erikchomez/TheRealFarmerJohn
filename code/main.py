try:
    from malmo import MalmoPython
except:
    import MalmoPython

import os
import sys
import time
import utils as uti

agent_host = MalmoPython.AgentHost()
mission_xml = uti.get_mission_xml()

# create default Malmo objects
try:
    agent_host.parse(sys.argv)
except RuntimeError as e:
    print('Error: ', e)
    print(agent_host.getUsage())
    exit(1)

if agent_host.receivedArgument('help'):
    print(agent_host.getUsage())
    exit(0)

my_mission = MalmoPython.MissionSpec(mission_xml, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# attempt to start a mission
max_retries = 3

for retry in range(max_retries):
    try:
        agent_host.startMission(my_mission, my_mission_record)
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print('Error starting mission: ', e)
            exit(1)
        else:
            time.sleep(2)

# loop until mission starts
print('Waiting for the mission to start ', end=' ')
world_state = agent_host.getWorldState()

while not world_state.has_mission_begun:
    print('.', end='')
    time.sleep(0.1)
    world_state = agent_host.getWorldState()

    for error in world_state.errors:
        print('Error: ', error.text)

print()

# loop until mission ends
print('Mission running ...')
while world_state.is_mission_running:
    time.sleep(0.1)
    world_state = agent_host.getWorldState()

    for error in world_state.errors:
        print('Error: ', error.text)

print('Mission ended')