def one_hot_action(env, action):
    import numpy as np
    ind = env.buttons.index(action)
    return np.array([int(i == ind) for i in range(len(env.buttons))])