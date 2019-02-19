__author__ = 'pascalpoizat'

from .SIGNAL import SIGNAL
from .Brick import Brick

class Action :
    """
    An action over a brick, sending a signal to it

    """

    def __init__(self, value: SIGNAL, brick: Brick):
        """
        Constructor.

        :param value: SIGNAL, the signal to send
        :param brick: Brick, the brick concerned by the action
        :return:
        """
        self.value: SIGNAL = value
        self.brick: Brick = brick
