from enum import Enum
from random import randrange


class MiniGame(Enum):
    T_REX = "/mini-games/t-rex/index.html"
    PONG = "/mini-games/pong/index.html"

    @staticmethod
    def random():
        rand = randrange(2)
        if rand == 0:
            return MiniGame.T_REX
        elif rand == 1:
            return MiniGame.PONG
        else:
            return MiniGame.T_REX
