import json
import logging
import sys
import random
import time

LOGGING = False  # set to True if you want to see more information


class TabQAgent(object):
    """ Tabular Q-learning agent for discrete state/action spaces"""

    def __init__(self):
        self.epsilon = 0.01  # chance of taking a random action instead of the best
        self.logger = logging.getLogger(__name__)

        if LOGGING:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        self.logger.handlers = []
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

        self.actions = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1"]
        self.q_table = {}
        self.canvas = None
        self.root = None

        self.prev_s = None
        self.prev_a = None

    def update_q_table(self, reward, current_state):
        """
        Change Q-table to reflect what we have learnt
        :param reward:
        :param current_state:
        :return:
        """
        # retrieve the old action value from the Q-table
        # indexed by the previous state and the previous action
        old_q = self.q_table[self.prev_s][self.prev_a]

        # assign the new action value
        new_q = reward + old_q

        # assign the new action value to the Q-table
        self.q_table[self.prev_s][self.prev_a] = new_q

    def update_q_table_from_terminating_state(self, reward):
        """
        Change Q-table to reflect what we have learnt after reaching a terminal state
        :param reward:
        :return:
        """
        old_q = self.q_table[self.prev_s][self.prev_a]

        # assign the new action value
        new_q = reward + old_q

        # assign the new action value to the Q-table
        self.q_table[self.prev_s][self.prev_a] = new_q

    def act(self, world_state, agent_host, current_r):
        """
        Take 1 action in response to the current world state
        :param world_state:
        :param agent_host:
        :param current_r:
        :return:
        """
        obs_text = world_state.observations[-1].text
        obs = json.loads(obs_text)  # most recent observation

        self.logger.debug(obs)

        if u'XPos' not in obs or u'ZPos' not in obs:
            self.logger.error("Incomplete observation received: %s" % obs_text)
            return 0

        current_s = "%d:%d" % (int(obs[u'XPos']), int(obs[u'ZPos']))

        self.logger.debug("State: %s (x = %.2f, z = %.2f)" % (current_s, float(obs[u'XPos']), float(obs[u'ZPos'])))

        if current_s not in self.q_table:
            self.q_table[current_s] = ([0] * len(self.actions))

        # update Q values
        if self.prev_s is not None and self.prev_a is not None:
            self.update_q_table(current_r, current_s)

        # TODO: implement drawing Q-Table
        # self.draw_Q(curr_x=int(obs[u'XPos']), curr_y=int(obs[u'ZPos']))

        # select the next action
        rnd = random.random()

        if rnd < self.epsilon:
            action = random.randint(0, len(self.actions) - 1)
            self.logger.info("Random action: %s" % self.actions[action])

        else:
            m = max(self.q_table[current_s])
            self.logger.debug("Current values: %s" % ",".join(str(x) for x in self.q_table[current_s]))

            actions_list = []

            for i in range(len(self.actions)):
                if self.q_table[current_s][i] == m:
                    actions_list.append(i)

            y = random.randint(0, len(actions_list) - 1)
            action = actions_list[y]

            self.logger.info("Taking q action: %s" % self.actions[action])

        # try to send the selected action
        # only update prev_s if this succeeds

        try:
            agent_host.sendCommand(self.actions[action])
            self.prev_s = current_s
            self.prev_a = action

        except RuntimeError as e:
            self.logger.error("Failed to send command: %s" % e)

        return current_r

    def run(self, agent_host):
        """
        Run the agent on the world
        :param agent_host: the agent
        :return:
        """
        total_reward = 0
        current_reward = 0

        self.prev_a = None
        self.prev_s = None

        is_first_action = True

        # main loop
        world_state = agent_host.getWorldState()

        while world_state.is_mission_running:
            if is_first_action:
                # wait until valid observation is received
                while True:
                    time.sleep(0.1)
                    world_state = agent_host.getWorldState()

                    # for error in world_state.errors:
                    #     self.logger.error("Error: %s" % error.text)
                    #
                    # for reward in world_state.rewards:
                    #     current_reward += reward.getValue()

                    current_reward = self._update_rewards(world_state, current_reward)

                    if world_state.is_mission_running and len(world_state.observations) > 0 and not \
                            world_state.observations[-1].text == '{}':
                        total_reward += self.act(world_state, agent_host, current_reward)
                        break

                    if not world_state.is_mission_running:
                        break

                is_first_action = False
            else:
                # wait for non-zero reward
                while world_state.is_mission_running and current_reward == 0:
                    time.sleep(0.1)
                    world_state = agent_host.getWorldState()

                    # for error in world_state.errors:
                    #     self.logger.error("Error: %s" % error.text)
                    #
                    # for reward in world_state.rewards:
                    #     current_reward += reward.getValue()

                    current_reward = self._update_rewards(world_state, current_reward)

                # allow time to stabilise after action
                while True:
                    time.sleep(0.1)
                    world_state = agent_host.getWorldState()

                    # for error in world_state.errors:
                    #     self.logger.error("Error: %s" % error.text)
                    #
                    # for reward in world_state.rewards:
                    #     current_reward += reward.getValue()

                    current_reward = self._update_rewards(world_state, current_reward)

                    if world_state.is_mission_running and len(world_state.observations) > 0 and not \
                            world_state.observations[-1].text == '{}':
                        total_reward += self.act(world_state, agent_host, current_reward)
                        break

                    if not world_state.is_mission_running:
                        break

        # process final reward
        self.logger.debug("Final reward: %d" % current_reward)

        total_reward += current_reward

        # update Q values
        if self.prev_s is not None and self.prev_a is not None:
            self.update_q_table_from_terminating_state(current_reward)

        # TODO: implement drawing Q-Table
        # self.draw_Q()

        return total_reward

    def _update_rewards(self, world_state, current_reward):
        """
        Update current reward with current world state observation
        Also update logger with any errors
        :param world_state:
        :param current_reward:
        :return:
        """
        for error in world_state.errors:
            self.logger.error("Error: %s" % error.text)

        for reward in world_state.rewards:
            current_reward += reward.getValue()

        return current_reward

    # TODO: implement draw_Q function
    # def draw_Q(self, curr_x=None, curr_y=None):
