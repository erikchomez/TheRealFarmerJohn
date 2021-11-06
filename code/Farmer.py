try:
    from malmo import MalmoPython
except:
    import MalmoPython

import json
# import logging
import sys
# import random
import utils as uti
import time
import gym
import numpy as np
from gym.spaces import Discrete, Box


class Farmer(gym.Env):
    def __init__(self, env_config):
        self.size = 50
        self.reward_density = 0.1
        self.penalty_density = 0.02
        self.obs_size = 3
        self.max_episode_steps = 2000
        self.log_frequency = 1

        self.action_dict = {
            0: 'move 1',
            1: 'turn 1',
            4: 'use 1'
        }

        # Rllib parameters
        # self.action_space = Discrete(len(self.action_dict))
        self.action_space = Box(-1, 1, shape=(len(self.action_dict),), dtype=np.float32)
        self.observation_space = Box(0, 1, shape=(self.obs_size * self.obs_size, ), dtype=np.float32)

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
        self.farmland_obs = None
        self.dirt_obs = None
        self.allow_break_action = False
        self.episode_step = 0
        self.episode_return = 0
        self.returns = []
        self.steps = []

    def init_malmo(self):
        my_mission = MalmoPython.MissionSpec(uti.get_mission_xml(), True)
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
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()

            for error in world_state.errors:
                print('\nError: ', error.text)

        return world_state

    def reset(self):
        """
        Reset environment for next episode
        :return:
        """
        # reset Malmo
        world_state = self.init_malmo()

        # reset variables
        self.returns.append(self.episode_return)
        current_step = self.steps[-1] if len(self.steps) > 0 else 0
        self.steps.append(current_step + self.episode_step)
        self.episode_return = 0
        self.episode_step = 0

        # log
        if len(self.returns) > self.log_frequency + 1 and len(self.returns) % self.log_frequency == 0:
            # self.log_returns()
            print('Logging')

        # get observation
        self.obs, self.allow_break_action = self.get_observation(world_state)

        return self.obs

    def step(self, action):
        # get action
        command_move = "move " + str(action[0])
        command_turn = "turn " + str(action[1])
        command_use = "use 1" if action[2] > 0.5 else "use 0"

        # check if any farmland is in front of agent
        if any(self.obs[:3]) and command_use == "use 1":
            self.agent_host.sendCommand("hotbar.2 1")
            self.agent_host.sendCommand("hotbar.2 0")

            self.agent_host.sendCommand(command_use)

        time.sleep(0.2)

        self.agent_host.sendCommand(command_move)
        self.agent_host.sendCommand(command_turn)

        self.episode_step += 1

        world_state = self.agent_host.getWorldState()

        for error in world_state.errors:
            print('Error: ', error.text)

        self.obs, self.allow_break_action = self.get_observation(world_state)

        # get done
        done = not world_state.is_mission_running

        # get reward
        reward = 0

        for r in world_state.rewards:
            reward += r.getValue()

        self.episode_return += reward

        return self.obs, reward, done, dict()

    def get_observation(self, world_state):
        obs = np.zeros((self.obs_size * self.obs_size, ))
        allow_break_action = False

        while world_state.is_mission_running:
            time.sleep(0.1)

            world_state = self.agent_host.getWorldState()

            if len(world_state.errors) > 0:
                raise AssertionError('Could not load grid')

            if world_state.number_of_observations_since_last_state > 0:
                # first we get json from observation API
                msg = world_state.observations[-1].text
                observations = json.loads(msg)
                # get observation
                grid = observations['floor3x3']
                # print('len grid: ', len(grid))
                for i, x in enumerate(grid):
                    obs[i] = x == 'farmland'
                # print('obs before ', obs)
                # rotate observations with orientation of agent
                obs = obs.reshape((3, 3))
                # print(obs)
                yaw = observations['Yaw']

                if 255 <= yaw < 315:
                    obs = np.rot90(obs, k=1)

                elif yaw >= 315 or yaw < 45:
                    obs = np.rot90(obs, k=2)

                elif 45 <= yaw < 135:
                    obs = np.rot90(obs, k=3)

                obs = obs.flatten()
                # print('obs after ', obs)
                allow_break_action = observations['LineOfSight']['type'] == 'farmland'

                break

        return obs, allow_break_action
