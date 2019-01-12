import retro
import retro.data
import numpy as np
import time
from drivingagent import TensorforceDrivingAgent
from startingagent import TensorforceStartingAgent
from playeragent import PlayerAgent
### SETTINGS
reload_model_if_existing = True
render_game = False

#Set up environment
env = retro.make('Dragster-Atari2600', inttype = retro.data.Integrations.EXPERIMENTAL_ONLY)

### UTILITIES
def one_hot_action(action):
    ind = env.buttons.index(action)
    size = len(env.buttons)
    return np.array([int(i == ind) for i in range(size)])

def are_all_values_zero(d):
    for k in d:
        if not d[k] == 0:
            return False
    return True

driving_agent_actions = ["LEFT",None,"BUTTON","LEFTandBUTTON"]
starting_agent_actions = [None,"BUTTON"]

#Create agents
driving_agent = TensorforceDrivingAgent(driving_agent_actions)
starting_agent = TensorforceStartingAgent(starting_agent_actions)
#agent = PlayerAgent(driving_agent_actions)
if reload_model_if_existing:
    driving_agent.load()
    starting_agent.load()
"""

    TRAINING

"""

max_reward = -10000
best_time_h_seconds = 100
best_time_seconds = 100
for epoch in range(1, 1000000000):
    env.reset()
    #Make a single "RIGHT" input to get an info object
    is_left_pressed = False
    observation, _, _, info = env.step(one_hot_action("RIGHT"))
    #Press right and NONE until we have a decently low countdown, so it's showing on screen
    while True:
        if render_game:
            env.render()
        if info["timeUntilStart"] >= 1 and info["timeUntilStart"] <= 30:
            break
        elif info["timeUntilStart"] > 0:
            observation, _, _, info = env.step(one_hot_action(None))
        else:
            observation, _, _, info = env.step(one_hot_action("RIGHT"))

    #Perform start
    start_failed = False
    start_reward = 0
    start_done = False
    while not start_done:
        #If not us, wait a frame
        if info["playerTurn"] == 1:
            observation, _, _, info = env.step(one_hot_action(None))
        else:
            agent_action = one_hot_action(starting_agent_actions[starting_agent.act(observation)])
            left_action = one_hot_action("LEFT")
            action = np.add(left_action, agent_action)

            observation, _, _, info = env.step(action)
            start_reward = 0
            if render_game:
                env.render()
            if info["p1Blown1"] == 1 and info["p1Blown2"] == 26:
                start_failed = True
                start_done = True
                start_reward = float(-info["timeUntilStart"])
            elif info["timeUntilStart"] <= 1:
                start_done = True

            if not start_done:
                starting_agent.observe(terminal=start_done, reward=start_reward)

    #If start succeeded, go on to driving-mode
    if not start_failed:
        driving_done = False
        driving_reward_sum = 0
        last_distance = 0
        blow_engine_penalty = -100

        while not driving_done:
            #If not us, wait a frame
            if info["playerTurn"] == 1:
                observation, _, _, info = env.step(one_hot_action(None))
            else:
                action = driving_agent_actions[driving_agent.act(observation)]
                if action == "LEFTandBUTTON":
                    action = np.add(one_hot_action("LEFT"), one_hot_action("BUTTON"))
                else:
                    action = one_hot_action(action)
                observation, _, _, info = env.step(action)

                if render_game:
                    env.render()

                """
                    FIGURE OUT DONE + REWARD AND PUNISHMENT
                """
                #Driving reward
                reward = 0
                #Did we blow the engine?
                if info["p1Blown1"] == 1 and info["p1Blown2"] == 26:
                    driving_done = True
                    reward = blow_engine_penalty
                #Did we hit 99.99s? Stop
                elif info["timeP1Seconds"] == 99 and info["timeP1HundredthOfSecond"] == 99:
                    driving_done = True
                #Did we finish the race? :)
                elif info["p1Distance"] == 97:
                    driving_done = True
                elif info["p1Distance"] > last_distance:
                    reward = 5 * (info["p1Distance"] - last_distance)
                    last_distance = info["p1Distance"]
                    blow_engine_penalty = blow_engine_penalty + 1
                else:
                    reward = -1

                driving_reward_sum = driving_reward_sum + reward

                #Reward agent
                driving_agent.observe(terminal=driving_done, reward=reward)

        start_reward = max(0, driving_reward_sum)

        #Print stuff!
        if driving_reward_sum > max_reward:
            max_reward = driving_reward_sum
        if info["p1Distance"] == 97 and (info["timeP1Seconds"] < best_time_seconds or info["timeP1Seconds"] == best_time_seconds and info["timeP1HundredthOfSecond"] < best_time_h_seconds):
            best_time_seconds = info["timeP1Seconds"]
            best_time_h_seconds = info["timeP1HundredthOfSecond"]
        print("Epoch "+str(epoch)+" over. Total reward: "+str(driving_reward_sum)+". Max reward so far: "+str(max_reward)+". Best time so far: "+(str(best_time_seconds)+":"+str(best_time_h_seconds)))
        print("Latest info object was: ")
        print(info)


    #And reward starter agent
    starting_agent.observe(terminal=True, reward=start_reward)

    if epoch%50 == 0:
        driving_agent.save_model()
        starting_agent.save_model()
