import retro
import retro.data
import numpy as np
from utilities import one_hot_action
from tensorforceagent import TensorforceAgent
from playeragent import PlayerAgent
from omniagent import OmniAgent

### SETTINGS
reload_model_if_existing = True #True: Try to reload an existing model
render_game = True #Will render and display game if true. False is faster

#Set up environment
env = retro.make('Dragster-Atari2600', inttype = retro.data.Integrations.EXPERIMENTAL_ONLY)
env.reset()

#Create agents
action_map = {
    None: one_hot_action(env, None),
    "LEFT": one_hot_action(env, "LEFT"),
    "BUTTON": one_hot_action(env, "BUTTON"),
    "RIGHT": one_hot_action(env, "RIGHT"),
    "LEFTandBUTTON": np.add(one_hot_action(env, "LEFT"), one_hot_action(env, "BUTTON")),
    "RESET": one_hot_action(env, "RESET")
}
agent_actions = ["LEFT",None,"BUTTON","LEFTandBUTTON"]
#agent = TensorforceAgent(agent_actions)
agent = OmniAgent(agent_actions)
#agent = PlayerAgent(agent_actions)
if reload_model_if_existing:
    agent.load()

"""

    TRAINING

"""

max_reward = -10000
best_time = 100.0
epoch = 1
while True:
    #Make a single "RIGHT" input to get an info object
    for i in range(0,2):
        observation, _, _, info = env.step(action_map["RIGHT"])
    #Press right and NONE until we have a decently low countdown, so it's showing on screen
    while True:
        if render_game:
            env.render()
        if info["timeUntilStart"] >= 1 and info["timeUntilStart"] <= 8:
            break
        elif info["timeUntilStart"] > 0:
            observation, _, _, info = env.step(action_map[None])
        else:
            observation, _, _, info = env.step(action_map["RIGHT"])
    #If start succeeded, go on to driving-mode
    driving_done = False
    driving_reward_sum = 0
    last_distance = 0
    while not driving_done:
        #If not us, wait a frame
        if info["playerTurn"] == 1:
            observation, _, _, info = env.step(action_map[None])
        else:
            agent_action = agent_actions[agent.act(observation)]
            action = action_map[agent_action]
            observation, _, _, info = env.step(action)

            #Make useful fields nicer
            info["p1Distance"] = info["p1Distance1"] + info["p1Distance2"]/float(256)
            info["p1Time"] = info["timeP1Seconds"] + info["timeP1HundredthOfSecond"] / 100.0
            del info["timeP1Seconds"]
            del info["timeP1HundredthOfSecond"]
            
            if render_game:
                env.render()

            """
                FIGURE OUT DONE + REWARD AND PUNISHMENT
            """
            reward = 0
            #Still counting down?
            if info["timeUntilStart"] > 0:
                #Started early?
                if info["p1StartedTooEarly"] == 29:
                    reward = -100 * info["timeUntilStart"]
                    driving_done = True
                else:
                    #We started successfully!
                    if info["timeUntilStart"] == 1:
                        reward = 700
                    else:
                        reward = 0
            else:
                #Driving reward
                reward = 0
                if info["p1Blown1"] == 1 and info["p1Blown2"] == 26:
                    reward = -100 + info["p1Distance1"]
                    driving_done = True

                #Did we hit >= 20s? Stop
                elif info["p1Time"] >= 20:
                    driving_done = True
                #Did we finish the race? :)
                elif info["p1Distance1"] >= 97:
                    driving_done = True
                    reward = 100
                elif info["p1Distance1"] > last_distance:
                    reward = 5
                    last_distance = info["p1Distance1"]
                else:
                    reward = -1
            
            driving_reward_sum = driving_reward_sum + reward

            #Reward agent
            agent.observe(terminal=driving_done, reward=reward)

    #Print stuff
    if driving_reward_sum > max_reward:
        max_reward = driving_reward_sum
    if info["p1Distance"] > 97 and info["p1Time"] < best_time:
        best_time = info["p1Time"]
    print("Epoch "+str(epoch)+" over. Total reward: "+str(driving_reward_sum)+". Max reward so far: "+str(max_reward)+". Best time so far: "+(str(best_time)))
    print("Latest info object was: ")
    print(info)
    print("")

    if epoch%100 == 0:
        agent.save_model()

    #Press reset twice to ensure environment has been reset
    for i in range(0, 2):
        observation, _, _, info = env.step(action_map["RESET"])
    env.reset()

    epoch = epoch + 1
