from tensorforce.agents import PPOAgent, DQNAgent
import scipy.misc
import numpy as np

class TensorforceAgent:
    def __init__(self,actions):
        preprocessing_config = [
            {
                "type": "grayscale"
            }
        ]
        exploration_config = dict(
            type="epsilon_anneal",
            initial_epsilon=0.25,
            final_epsilon=0.01,
            timesteps=1000000
        )

        network_spec = [
            dict(type='conv2d', size=16, window=8, stride=4, activation='lrelu'),
            dict(type='conv2d', size=32, window=4, stride=2, activation='lrelu'),
            dict(type='flatten'),
            dict(type='dense', size=256, activation='lrelu')
        ]
        self.network_path = "network/"
        self.agent = PPOAgent(
            actions = dict(type='int', num_actions=len(actions)),
            states = dict(type='float', shape=(35, 150, 3)),
            network = network_spec,
            actions_exploration = exploration_config,
            states_preprocessing = preprocessing_config
        )

    def act(self, obs):
        #Cut out only the part needed
        partly = np.delete(obs, np.s_[96:], 0)
        partly = np.delete(partly, np.s_[0:26], 0)
        partly = np.delete(partly, np.s_[35:45], 0)
        partly = np.delete(partly, np.s_[38:53], 0)
        partly = np.delete(partly, np.s_[31:35], 0)
        partly = np.delete(partly, np.s_[10:16], 0)
        frame = np.delete(partly, np.s_[150:], 1)

        #scipy.misc.imsave('outfile.jpg', frame)

        return self.agent.act(frame)

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
