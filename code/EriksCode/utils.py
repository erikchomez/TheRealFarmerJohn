# /Users/erikgomez/MalmoPlatform/Python_Examples/checkpoint-260-good-agent
# /Users/erikgomez/MalmoPlatform/Python_Examples/checkpoint-efficiency

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
    def generate_enclosed_area() -> str:
        """
        Generates the enclosed area for the agent which includes:
        5x5 grid of farmland
        Fences surrounding farmland with 1 block gap
        """
        # reset "<DrawCuboid x1='{}' x2='{}' y1='2' y2='2' z1='{}' z2='{}' type='air'/>".format(-4, 4, -4, 4) + \
        farmland = "<DrawCuboid x1='{}' x2='{}' y1='1' y2='1' z1='{}' z2='{}' type='farmland'/>".format(-2, 2, -2, 2)

        # generate the outer fences
        fences = WorldGenerator.generate_fences()

        # single water block can hydrate 9x9 grid so set it to the middle of our farmland
        single_water_block = "<DrawBlock x='{}' y='1' z='{}' type='water'/>".format(0, 0)
        single_slab_block = "<DrawBlock x='{}' y='2' z='{}' type='wooden_slab'/>".format(0, 0)

        return fences + farmland + single_water_block + single_slab_block

    @staticmethod
    def generate_fences():
        """
        Generates the 9x9 grid of outer fences
        """
        fence_block = "<DrawBlock x='{}' y='2' z='{}' type='fence'/>"
        torch_block = "<DrawBlock x='{}' y='2' z='{}' type='torch'/>"
        fences = ''
        torches = ''

        for i in range(-4, 5):
            fences += fence_block.format(-4, i)
            fences += fence_block.format(4, i)
            fences += fence_block.format(i, 4)
            fences += fence_block.format(i, -4)

        for i in range(-3, 4):
            torches += torch_block.format(-3, i)
            torches += torch_block.format(3, i)
            torches += torch_block.format(i, 3)
            torches += torch_block.format(i, -3)

        return fences + torches

    def gen_fertile_wasteland(self, size: int, density: int) -> str:
        """
        Generate a plane of land that contains dirt,
        tilled soil, and water. String returned
        is Malmo-friendly XML.
        """
        wasteland_xml = f"{self._rand_blocks(size=size, height=1, density=density, block_type='dirt')}"
        return wasteland_xml

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
    def get_mission_xml():
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
                    <MsPerTick>2</MsPerTick>
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
               WorldGenerator.generate_enclosed_area() + \
               '''</DrawingDecorator>
                      <ServerQuitFromTimeUp timeLimitMs="4600000"/>
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
                      <RewardForDiscardingItem>
                        <Item reward="1" type="wheat_seeds"/>
                      </RewardForDiscardingItem>
                      <RewardForCollectingItem>
                        <Item reward="1" type="wheat"/>
                        <Item reward="-1" type="torch"/>
                      </RewardForCollectingItem>
                      <ContinuousMovementCommands/>
                      <InventoryCommands/>
                      <ObservationFromFullStats/>
                      <ObservationFromRay/>
                      <ObservationFromGrid>
                        <Grid name="floor3x3">
                            <min x="-1" y="0" z="-1"/>
                            <max x="1" y="0" z="1"/>
                        </Grid>
                        <Grid name="farmland_grid" absoluteCoords="true">
                            <min x="-2" y="2" z="-2"/>
                            <max x="2" y="2" z="2"/>
                        </Grid>
                      </ObservationFromGrid>
                    </AgentHandlers>
                  </AgentSection>
                </Mission>'''
