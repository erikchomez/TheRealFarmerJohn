try:
    from malmo import MalmoPython
except:
    import MalmoPython

import json
# import logging
import sys
import random
import math
from generation.utils import WorldGenerator
import time
import gym
import os
import numpy as np
from gym.spaces import Discrete, Box
import matplotlib.pyplot as plt


class Farmer(gym.Env):
    def __init__(self, env_config):
        self.size = 50
        self.reward_density = 0.1
        self.penalty_density = 0.02
        self.obs_size = 5
        self.max_episode_steps = 500
        self.log_frequency = 1

        self.world_gen = WorldGenerator()
        self.save_path = '\Malmo\proj'
        self.debug = True

        self.action_dict = {
            0: 'move 1',
            1: 'turn 1',
            2: 'use 1',
            3: 'jump 1',
            4: 'switch 1',
            5: 'attack 1'
        }

        # Rllib parameters
        # self.action_space = Discrete(len(self.action_dict))
        self.action_space = Box(-1, 1, shape=(len(self.action_dict),), dtype=np.float32)
        self.observation_space = Box(0, 1, shape=(2 * self.obs_size * self.obs_size, ), dtype=np.float32)

        # Malmo parameters
        self.agent_host = MalmoPython.AgentHost()

        try:
            self.agent_host.parse(sys.argv)

        except RuntimeError as e:
            print('Error: ', e)
            print(self.agent_host.getUsage())
            exit(1)

        # Farmer parameters
        self.obs = None
        self.allow_break_action = False
        self.in_water_block = False
        self.episode_step = 0
        self.episode_return = 0
        self.returns = []
        self.steps = []

    def init_malmo(self):
        size = 50
        world = self.world_gen.gen_fertile_wasteland(size, 0.1)
        fences = self.world_gen.generate_enclosed_area(size, 'fence')
        border = self.world_gen.generate_enclosed_area(size + 1, 'cobblestone')
        border += self.world_gen.generate_enclosed_area(size + 2, 'cobblestone')
        my_mission = MalmoPython.MissionSpec(self.world_gen.get_mission_xml(world + fences + border), True)
        my_mission_record = MalmoPython.MissionRecordSpec()
        my_mission.requestVideo(800, 500)
        my_mission.setViewpoint(1)

        max_retries = 3
        my_clients = MalmoPython.ClientPool()
        my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000))

        for retry in range(max_retries):
            try:
                self.agent_host.startMission(my_mission, my_clients, my_mission_record, 0, 'Farmer')
                break

            except RuntimeError as e:
                if retry == max_retries - 1:
                    print('Error starting mission: ', e)
                    exit(1)
                else:
                    time.sleep(2)

        world_state = self.agent_host.getWorldState()

        while not world_state.has_mission_begun:
            world_state = self.agent_host.getWorldState()

            for error in world_state.errors:
                print('\nError: ', error.text)

        # main loop
        if self.debug:
            print("Starting To Farm")

        return world_state

    def reset(self):
        """
        Reset environment for next episode
        :return:
        """
        # reset Malmo
        world_state = self.init_malmo()

        # reset variables
        self.agent_host.sendCommand('/effect @a 23 99999 10')  # disable hunger
        self.returns.append(self.episode_return)
        current_step = self.steps[-1] if len(self.steps) > 0 else 0
        self.steps.append(current_step + self.episode_step)
        self.episode_return = 0
        self.episode_step = 0
        self.in_water_block = False
        # log
        if len(self.returns) > self.log_frequency + 1 and len(self.returns) % self.log_frequency == 0:
            self.log_returns()
            if self.debug:
                print('Logging')

        # get observation
        self.obs = self.get_observation(world_state)

        return self.obs

    def step(self, action):
        # get action
        command_move = "move " + str(action[0])
        command_turn = "turn " + str(action[1])
        command_jump = "jump 1" if action[3] > 0.5 else "jump 0"
        command_attack = "attack 1" if action[5] > 0.5 else "attack 0"

        # Use command
        item_slot = math.ceil(abs(action[4]) * 10)
        if item_slot > 9:
            item_slot = 9
        self._use_hotbar(item_slot)

        self.agent_host.sendCommand(command_move)
        self.agent_host.sendCommand(command_turn)
        self.agent_host.sendCommand(command_jump)
        self.agent_host.sendCommand(command_attack)
        self.agent_host.sendCommand('chat /effect @a 23 99999 10')
        self.agent_host.sendCommand('chat /weather clear')
        time.sleep(0.001) # sleep for 20 ticks, which is normally 1 second

        self.episode_step += 1
        world_state = self.agent_host.getWorldState()

        for error in world_state.errors:
            if self.debug:
                print('Error: ', error.text)

        self.obs = self.get_observation(world_state)

        # get done
        done = not world_state.is_mission_running

        # get reward
        step_reward = 0
        for r in world_state.rewards:
            reward = r.getValue()
            step_reward += reward
        self.episode_return += step_reward

        return self.obs, step_reward, done, dict()

    def _use_hotbar(self, hotbar_key):
        """
        Switch to hotbar item at hotbar_key
        Hotbar is 0-indexes, but commands are 1-indexed
        """
        command = "hotbar.{} {}"

        # press key and release key
        for i in reversed(range(2)):
            self.agent_host.sendCommand(command.format(hotbar_key, i))

        # send command to use item in hotbar
        self.agent_host.sendCommand("use 1")

    def get_observation(self, world_state):
        """
        Get world observations
        Will be using 2x25x25 grid, rotated depending on the orientation of the agent
        """

        obs = np.zeros((2 * self.obs_size * self.obs_size, ))
        while world_state.is_mission_running:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            if len(world_state.errors) > 0:
                raise AssertionError('Could not load grid')

            if world_state.number_of_observations_since_last_state > 0:
                msg = world_state.observations[-1].text
                
                observations = json.loads(msg)
                grid = observations['floorAll']
                for i, x in enumerate(grid):
                    obs[i] = x == 'farmland' or x == 'wheat' or x == 'dirt' or x == 'grass' or x == 'water'
                
                obs = obs.reshape((2, self.obs_size, self.obs_size))
                # if agent falls into water block
                if observations['YPos'] == 1.0:
                    self.in_water_block = True
                else:
                    self.in_water_block = False

                # rotate observations with orientation of agent
                yaw = observations['Yaw']
                # rotate on axes=(1,2) so we can have farmland observations at the top
                if 255 <= yaw < 315:
                    obs = np.rot90(obs, k=1, axes=(1, 2))
                elif yaw >= 315 or yaw < 45:
                    obs = np.rot90(obs, k=2, axes=(1, 2))

                elif 45 <= yaw < 135:
                    obs = np.rot90(obs, k=3, axes=(1, 2))
                obs = obs.flatten()

                break

        return obs

    def log_returns(self):
        """
        Log the current returns as a graph and text file

        Args:
            steps (list): list of global steps after each episode
            returns (list): list of total return of each episode
        """
        save_path = self.save_path
        box = np.ones(self.log_frequency) / self.log_frequency
        returns_smooth = np.convolve(self.returns[1:], box, mode='same')
        plt.clf()
        plt.plot(self.steps[1:], returns_smooth)
        plt.title('Farmer: Seed Planting')
        plt.ylabel('Return')
        plt.xlabel('Steps')
        plt.savefig(os.path.join(save_path, 'returns.png'))

        with open(os.path.join(save_path, 'returns.txt'), 'w') as f:
            for step, value in zip(self.steps[1:], self.returns[1:]):
                f.write("{}\t{}\n".format(step, value))
