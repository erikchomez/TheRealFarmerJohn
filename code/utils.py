
def generate_enclosed_area():
    """
    Generates the enclosed area for the agent which includes:
    5x5 grid of farmland
    Fences surrounding farmland with 1 block gap
    """
    # reset "<DrawCuboid x1='{}' x2='{}' y1='2' y2='2' z1='{}' z2='{}' type='air'/>".format(-4, 4, -4, 4) + \
    farmland = "<DrawCuboid x1='{}' x2='{}' y1='1' y2='1' z1='{}' z2='{}' type='farmland'/>".format(-2, 2, -2, 2)

    fence_block = "<DrawBlock x='{}' y='2' z='{}' type='fence'/>"
    fences = ''

    for i in range(-4, 5):
        fences += fence_block.format(-4, i)
        fences += fence_block.format(4, i)
        fences += fence_block.format(i, 4)
        fences += fence_block.format(i, -4)

    return fences + farmland


def get_mission_xml():
    """
    Initial mission used for basic training
    Agent starts off in an enclosed area with a hoe and a few other resources
    """
    return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>RL + Curriculum Learning</Summary>
              </About>

              <ServerSection>
                <ServerInitialConditions>
                  <Time>
                    <StartTime>0</StartTime>
                  </Time>
                  <Weather>clear</Weather>
                </ServerInitialConditions>
              
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,2;1;"/>
                  <DrawingDecorator>''' + \
                    generate_enclosed_area() + \
                  '''</DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="10000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              <AgentSection mode="Survival">
                <Name>CS175 Farmer</Name>
                <AgentStart>
                  <Placement x="0" y="2" z="-3" pitch="45" yaw="0"/>
                    <Inventory>
                      <InventoryItem slot="0" type="diamond_hoe"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''
