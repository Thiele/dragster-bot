class OmniAgent:
    """
        Implementation of this strategy:
        https://docs.google.com/spreadsheets/d/1m1JKUGQdqjRkgqWgY6j6Dp1dXqM7KKEuYwjw7fpnLSM/edit#gid=1438444937
    """
    __base_framecounter = -4
    __frame_counter = __base_framecounter
    def __init__(self,actions):
        self.actions = actions

    def act(self, observation):
        action = None
        if self.__frame_counter < 0:
            action = self.actions.index("LEFTandBUTTON")
        elif self.__frame_counter < 14:
            action = self.actions.index("BUTTON")
        elif self.__frame_counter == 14:
            action = self.actions.index("LEFTandBUTTON")
        elif self.__frame_counter < 18:
            action = self.actions.index(None)
        elif self.__frame_counter < 29:
            action = self.actions.index("BUTTON")
        elif self.__frame_counter == 29:
            action = self.actions.index("LEFTandBUTTON")
        elif self.__frame_counter < 53:
            action = self.actions.index("BUTTON")
        elif self.__frame_counter == 53:
            action = self.actions.index("LEFTandBUTTON")
        elif self.__frame_counter < 75:
            action = self.actions.index("BUTTON")
        elif self.__frame_counter == 75:
            action = self.actions.index("LEFTandBUTTON")
        elif self.__frame_counter < 86:
            action = self.actions.index("BUTTON")
        elif self.__frame_counter == 86:
            action = self.actions.index("LEFTandBUTTON")
        elif self.__frame_counter < 99:
            action = self.actions.index("BUTTON")
        elif self.__frame_counter == 99:
            action = self.actions.index("LEFTandBUTTON")
        elif self.__frame_counter < 108:
            action = self.actions.index("BUTTON")
        elif self.__frame_counter == 108:
            action = self.actions.index("LEFTandBUTTON")
        elif self.__frame_counter < 117:
            action = self.actions.index("BUTTON")
        elif self.__frame_counter == 117:
            action = self.actions.index("LEFTandBUTTON")
        elif self.__frame_counter < 139:
            action = self.actions.index("BUTTON")
        elif self.__frame_counter < 152:
            action = self.actions.index("LEFT")
        elif self.__frame_counter == 152:
            action = self.actions.index("LEFTandBUTTON")
        elif self.__frame_counter < 160:
            action = self.actions.index("LEFT")
        elif self.__frame_counter == 160:
            action = self.actions.index("LEFTandBUTTON")
        elif self.__frame_counter < 167:
            action = self.actions.index("LEFT")

        self.__frame_counter = self.__frame_counter + 1
        return action

    def observe(self, terminal = False, reward = 0):
        if terminal:
            input("Game won. Enter anything to do it again")
            self.__frame_counter = self.__base_framecounter
        return None

    def load(self):
        pass

    def save_model(self):
        pass
