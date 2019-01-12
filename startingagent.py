from tensorforce.agents import PPOAgent, DQNAgent
import numpy as np

class TensorforceStartingAgent:
    def __init__(self,actions):
        preprocessing_config = [
            {
                "type": "grayscale"
            },
            {
                "type": "divide",
                "scale": 255
            }
        ]
        exploration_config = dict(
            type="epsilon_decay",
            initial_epsilon=1.0,
            final_epsilon=0.1,
            timesteps=100000
        )
        """
        exploration_config = dict(
            type="constant",
            constant=0.1
        )
        """
        network_spec = [
            dict(type='conv2d', size=16, window=6, stride=3, activation='relu'),
            dict(type='flatten'),
            dict(type='dense', size=16, activation='relu')
        ]
        self.network_path = "starting-network/"
        self.agent = PPOAgent(
            actions = dict(type='int', num_actions=len(actions)),
            states = dict(type='float', shape=(32,160,3)),
            network = network_spec,
            #batched_observe = False,
            batching_capacity = 1500,
            actions_exploration = exploration_config,
            states_preprocessing = preprocessing_config
        )

    def act(self, obs):
        partly = np.delete(obs, np.s_[98:], 0)
        partly = np.delete(partly, np.s_[0:66], 0)

        return self.agent.act(partly)

    def load(self):
        import os
        if os.path.isdir(self.network_path):
            try:
                self.agent.restore_model(self.network_path)
            except:
                print("Failed to load model")

    def observe(self, terminal = False, reward = 0):
        return self.agent.observe(terminal, reward)

    def save_model(self):
        import os
        if not os.path.isdir(self.network_path):
            os.makedirs(self.network_path)
        self.agent.save_model(self.network_path)
