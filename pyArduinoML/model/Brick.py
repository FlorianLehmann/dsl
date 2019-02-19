__author__ = 'pascalpoizat'

from pyArduinoML.model.NamedElement import NamedElement

class Brick(NamedElement):
    """
    Abstraction for bricks.

    """

    def __init__(self, name: str, pin: int):
        """
        Constructor.

        :param name: String, name of the brick
        :param pin: Integer, pin where the brick is connected
        :return:
        """
        NamedElement.__init__(self, name)
        self.pin: int = pin

    def declare(self):
        """
        Arduino code for the declaration of the brick.

        :return: String
        """
        return "int %s = %d;" % (self.name, self.pin)
