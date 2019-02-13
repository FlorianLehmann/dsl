__author__ = 'pascalpoizat'

from pyArduinoML.model.Transition import Transition
from pyArduinoML.model.TemporalComparison import TemporalComparison
from pyArduinoML.model.AnalogicComparison import AnalogicComparison
from pyArduinoML.model.DiscreteComparison import DiscreteComparison


class TransitionBuilder:
    """
    Builder for transitions.
    """

    def __init__(self, root, sensor):
        """
        Constructor.

        :param root: BehaviorBuilder, root builder
        :param sensor: String, name of the brick used to trigger the transition
        :return:
        """
        self.root = root
        self.sensor = sensor
        self.value = None  # SIGNAL, state of the brick to trigger the transition
        self.next_state = None  # String, name of the target state

    def has_value(self, value):
        """
        Sets the action.

        :param value: SIGNAL, state of the brick to trigger the transition
        :return: TransitionBuilder, the builder
        """
        self.value = value
        return self

    def has_value(self, value):
        """
        Sets the action.

        :param value: SIGNAL, state of the brick to trigger the transition
        :return: TransitionBuilder, the builder
        """
        self.value = value
        return self

    def go_to_state(self, next_state):
        """
        Sets the target state.

        :param next_state: String, name of the target state
        :return: StateBuilder, the builder root
        """
        self.next_state = next_state
        return self.root.root

    def get_contents(self, bricks, states):
        
        tempo = TemporalComparison(5000)
        discrete = DiscreteComparison(bricks[self.sensor], self.value)

        return Transition(states[self.next_state], [tempo, discrete])
