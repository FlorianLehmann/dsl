__author__ = 'pascalpoizat'

from pyArduinoML.model.NamedElement import NamedElement
from pyArduinoML.model import SIGNAL
from .Transition import Transition

class State(NamedElement):
    """
    A state in the application.

    """

    def __init__(self, name: str, actions: tuple=(), transition: Transition=None):
        """
        Constructor.

        :param name: String, name of the state
        :param actions: List[Action], sequence of actions to do when entering the state (size should be > 0)
        :param transition: Transition, unique outgoing transition
        :return:
        """
        NamedElement.__init__(self, name)
        self.transition: Transition = transition
        self.actions: tuple = actions

    def settransition(self, transition: Transition):
        """
        Sets the transition of the state
        :param transition: Transition
        :return:
        """
        self.transition = transition

    def setup(self):
        """
        Arduino code for the state.

        :return: String
        """
        rtr = ""
        rtr += "void state_%s() {\n" % self.name
        # generate code for state actions
        for action in self.actions:
            rtr += "\tdigitalWrite(%s, %s);\n" % (action.brick.name, action.value.__str__())
            rtr += "\tboolean guard =  millis() - time > debounce;\n"
        # generate code for the transition
        transition = self.transition
        rtr += transition.setup() + "else {\n\t\tstate_%s();\n\t}" % (self.name)
        # end of state
        rtr += "\n}\n"
        return rtr
