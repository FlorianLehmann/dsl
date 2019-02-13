__author__ = 'pascalpoizat'

from pyArduinoML.model.NamedElement import NamedElement
from pyArduinoML.model import SIGNAL
from .Transition import Transition

class State(NamedElement):
    """
    A state in the application.

    """

    def __init__(self, name: str, actions: tuple=(), transitions: tuple = ()):
        """
        Constructor.

        :param name: String, name of the state
        :param actions: List[Action], sequence of actions to do when entering the state (size should be > 0)
        :param transition: Transition, unique outgoing transition
        :return:
        """
        NamedElement.__init__(self, name)
        self.transitions: tuple = transitions
        self.actions: tuple = actions

    def setup(self):
        """
        Arduino code for the state.

        :return: String
        """
        rtr = ""
        rtr += "void state_%s() {\n" % self.name
        # generate code for state actions
        for action in self.actions:
            rtr += "\tdigitalWrite(%s, %s);\n" % (action.brick.name, str(action.value))
            rtr += "\tboolean guard =  millis() - time > debounce;\n"
        # generate code for the transition

        for transition in self.transitions:
            rtr += transition.setup()
        # end of state
        rtr += "\n}\n"
        return rtr
