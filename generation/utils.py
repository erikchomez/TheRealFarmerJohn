import numpy as np


class WorldGenerator:

    """
    WorldGenerator class is used for generating
    Malmo XML information and ultimately
    generating Minecraft terrain.
    """

    def __init__(self):
        pass

    @staticmethod
    def generate_enclosed_area(size: int, block_type: str) -> str:
        fence_block = "<DrawBlock x='{}' y='2' z='{}' type='{}'/>"
        fences = ''

        for i in range(-1 * size, size):
            fences += fence_block.format(-1 * size + 1, i + 1, block_type)
            fences += fence_block.format(size, i + 1, block_type)
            fences += fence_block.format(i + 1, size, block_type)
            fences += fence_block.format(i + 1, -1 * size + 1, block_type)

        return fences

    def gen_fertile_wasteland(self, size: int, density: int) -> str:
        """
        Generate a plane of land that contains dirt,
        tilled soil, and water. String returned
        is Malmo-friendly XML.
        """
        wasteland_xml = f"{self._rand_blocks(size=size, height=1, density=density, block_type='water')}"
        return wasteland_xml

    def gen_fertile_land(self, size: int):
        fertile_xml = str()
        fertile_xml += self._generate_grid(size, 2, 'water')
        fertile_xml += self._generate_grid(size, 3, 'grass')
        return fertile_xml

    @staticmethod
    def _rand_blocks(size: int, height: int, density: int, block_type: str) -> str:
        """
        Generate a plane of random blocks (height,
        type, and density defined in parameters)
        in a square of size (size*size).

        Return proper Malmo XML to generate said blocks.
        """
        rand_grid = np.random.rand(size, size)
        cuboid_xml = str()
        for x, row in enumerate(rand_grid):
            for y, val in enumerate(row):
                if val < density:
                    cuboid_xml += f"<DrawBlock x='{x - size // 2}' y='{height}' z='{y - size // 2}' type='{block_type}'/>\n "
        return cuboid_xml

    @staticmethod
    def _generate_grid(size: int, height: int, block_type: str):
        rand_grid = np.random.rand(size, size)
        cuboid_xml = str()
        for x, row in enumerate(rand_grid):
            for y, val in enumerate(row):
                cuboid_xml += f"<DrawBlock x='{x - size // 2}' y='{height}' z='{y - size // 2}' type='{block_type}'/>\n "
        return cuboid_xml

    @staticmethod
    def get_mission_xml(custom_land: str):
        """
        Generate a flat plane of grass in Malmo
        XML. Custom world-generation information
        can be passed as a string.
        """

        return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    
                  <About>
                    <Summary>RL + Curriculum Learning</Summary>
                  </About>
                  
                  <ModSettings>
                    <MsPerTick>1</MsPerTick>
                  </ModSettings>
    
                  <ServerSection>
                    <ServerInitialConditions>
                      <Time>
                        <StartTime>0</StartTime>
                      </Time>
                      <Weather>clear</Weather>
                    </ServerInitialConditions>
                  
                    <ServerHandlers>
                      <FlatWorldGenerator generatorString="3;7,2;1;" forceReset="true"/>
                      <DrawingDecorator>''' + \
                        f"{custom_land}" + \
               '''</DrawingDecorator>
                      <ServerQuitFromTimeUp timeLimitMs="5500000"/>
                      <ServerQuitWhenAnyAgentFinishes/>
                    </ServerHandlers>
                  </ServerSection>
                  <AgentSection mode="Survival">
                    <Name>CS175 Farmer</Name>
                    <AgentStart>
                      <Placement x="0" y="2" z="-3" pitch="45" yaw="0"/>
                        <Inventory>
                          <InventoryItem slot="0" type="diamond_hoe"/>
                          <InventoryItem slot="1" type="wheat_seeds" quantity="64"/>
                          <InventoryItem slot="2" type="wheat_seeds" quantity="64"/>
                          <InventoryItem slot="3" type="wheat_seeds" quantity="64"/>
                          <InventoryItem slot="4" type="wheat_seeds" quantity="64"/>
                          <InventoryItem slot="5" type="wheat_seeds" quantity="64"/>
                        </Inventory>
                    </AgentStart>
                    <AgentHandlers>
                      <RewardForCollectingItem>
                        <Item reward="1" type="wheat"/>
                      </RewardForCollectingItem>
                      <RewardForTouchingBlockType>
                        <Block type="cobblestone" reward="-1"></Block>
                      </RewardForTouchingBlockType>
                      <AgentQuitFromTouchingBlockType>
                        <Block type="cobblestone"/>
                      </AgentQuitFromTouchingBlockType>
                      <ContinuousMovementCommands/>
                      <InventoryCommands/>
                      <ObservationFromFullStats/>
                      <ObservationFromRay/>
                      <ObservationFromGrid>
                        <Grid name="floor3x3">
                            <min x="-1" y="-1" z="-1"/>
                            <max x="1" y="-1" z="1"/>
                        </Grid>
                      </ObservationFromGrid>
                    </AgentHandlers>
                  </AgentSection>
                </Mission>'''
