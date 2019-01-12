import retro
import retro.data

#Set up environment
env = retro.make('Dragster-Atari2600', inttype = retro.data.Integrations.EXPERIMENTAL_ONLY)

actions = {
        "b": [1, 0, 0, 0, 0, 0, 0, 0],
        "bl":[1, 0, 0, 0, 0, 0, 1, 0],
        "l": [0, 0, 0, 0, 0, 0, 1, 0],
        "r": [0, 0, 0, 0, 0, 0, 0, 1],
        "0": [0, 0, 0, 0, 0, 0, 0, 0]
    }

def get_input():
    while True:
        print("Enter action. l = left, r = right, b = button, bl = button and left, 0 for no input")
        action = input()
        if action in actions:
            return actions[action]
        else:
            print("Bad input: "+action)

while True:
    env.reset()
    _, _, _, info = env.step(actions["0"])
    if info["playerTurn"] == 1:
        _, _, _, info = env.step(actions["0"])
    _, _, _, info = env.step(actions["r"])
    while True:
        env.render()
        _, _, _, info = env.step(get_input())
        print(info)
        if info["playerTurn"] == 1:
            _, _, _, info = env.step(actions["0"])