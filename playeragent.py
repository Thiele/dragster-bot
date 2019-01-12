class PlayerAgent:
    def __init__(self,actions):
        self.actions = actions

    def act(self, observation):
        print("Please act with one of the following ints:")
        for i in range(len(self.actions)):
            print(str(i)+": "+str(self.actions[i]))
        r = input("Enter action...")
        if r is None or r == '':
            r = self.actions.index(None)
        return int(r)

    def observe(self, terminal = False, reward = 0):
        print("Is terminal: "+str(terminal)+", reward was: "+str(reward))
        return None

    def load(self):
        pass

    def save_model(self):
        pass
