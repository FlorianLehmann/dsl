from pyArduinoML.antlr.ArduinomlListener import ArduinomlListener
from pyArduinoML.antlr.ArduinomlParser import ArduinomlParser

from pyArduinoML.model.Action import Action
from pyArduinoML.model.Actuator import Actuator
from pyArduinoML.model.AnalogicComparison import AnalogicComparison
from pyArduinoML.model.AnalogicOperator import AnalogicOperator
from pyArduinoML.model.App import App
from pyArduinoML.model.DiscreteComparison import DiscreteComparison
from pyArduinoML.model.DigitalSensor import DigitalSensor
from pyArduinoML.model.Mode import Mode
from pyArduinoML.model.Monitor import Monitor
from pyArduinoML.model.SIGNAL import SIGNAL
from pyArduinoML.model.State import State
from pyArduinoML.model.TemporalComparison import TemporalComparison
from pyArduinoML.model.Transition import Transition
from pyArduinoML.model.Brick import Brick


class _Mode:
    def __init__(self, name):
        self.name = name
        self.states = []
        self.transitions = []
    
    def bind(self, modes):
        transitions = tuple(transition.bind(modes) for transition in self.transitions)
        states = tuple(state.bind(self.states) for state in self.states)
        return Mode(self.name, transitions, states)
    
    def __repr__(self):
        return f'Mode({self.name}, {self.states}, {self.transitions})'


class _State:
    def __init__(self, name):
        self.name = name
        self.actions = []
        self.transitions = []
    
    def bind(self, states):
        transitions = tuple(transition.bind(states) for transition in self.transitions)
        return State(self.name, tuple(self.actions), transitions)

    def __repr__(self):
        return f'State({self.name}, {self.actions}, {self.transitions})'


class _Transition:
    def __init__(self, next_state):
        self.next_state = next_state
        self.comparaisons = []
    
    def bind(self, states):
        for state in states:
            if state.name == self.next_state:
                return Transition(state, tuple(self.comparaisons))
        raise RuntimeError(f'Unknown state {self.next_state}')
    
    def __repr__(self):
        return f'Transition({self.next_state}, {self.comparaisons})'


class Listener(ArduinomlListener):
    def __init__(self):
        super().__init__()
        self.app = None
        self.name = None
        self.monitor = Monitor()
        self.bricks = []
        self.modes = []

    def exitRoot(self, ctx:ArduinomlParser.RootContext):
        self.modes = tuple(mode.bind(self.modes) for mode in self.modes)
        for mode in self.modes:
            self.monitor.addMode(mode)
        self.app = App(self.name, tuple(self.bricks), self.modes, self.monitor)

    def enterShowStateMachine(self, ctx:ArduinomlParser.ShowStateMachineContext):
        self.monitor.showStateMachine = True

    def enterDeclaration(self, ctx:ArduinomlParser.DeclarationContext):
        self.name = ctx.name.text

    def enterSensor(self, ctx:ArduinomlParser.SensorContext):
        sensor = DigitalSensor(ctx.location().identifier.text, int(ctx.location().port.text))
        self.checkDebugOption(sensor, ctx)
        self.bricks.append(sensor)
    
    def enterActuator(self, ctx:ArduinomlParser.ActuatorContext):
        actuator = Actuator(ctx.location().identifier.text, int(ctx.location().port.text))
        self.checkDebugOption(actuator, ctx)
        self.bricks.append(actuator)

    def exitInitialMode(self, ctx:ArduinomlParser.InitialModeContext):
        self.modes.insert(0, self.modes.pop(-1))

    def enterCustomMode(self, ctx:ArduinomlParser.CustomModeContext):
        mode_name = ctx.identifier.text
        self.modes.append(_Mode(mode_name))

    def exitInitialState(self, ctx:ArduinomlParser.InitialStateContext):
        self.modes[-1].states.insert(0, self.modes[-1].states.pop(-1))

    def enterCustomState(self, ctx:ArduinomlParser.CustomStateContext):
        state_name = ctx.identifier.text
        self.modes[-1].states.append(_State(state_name))

    def enterAction(self, ctx:ArduinomlParser.ActionContext):
        receiver = ctx.receiver.text
        value = SIGNAL(ctx.value.text)
        self.modes[-1].states[-1].actions.append(Action(receiver, value))

    def enterStateTransition(self, ctx:ArduinomlParser.StateTransitionContext):
        next_state = ctx.next_state.text
        self.modes[-1].states[-1].transitions.append(_Transition(next_state))

    def enterAnalogicComparison(self, ctx:ArduinomlParser.AnalogicComparisonContext):
        trigger = ctx.trigger.text
        for brick in self.bricks:
            if brick.name == trigger:
                sensor = brick
                break
        else:
            raise RuntimeError(f'Unknown sensor {trigger}')
        operator = AnalogicOperator(ctx.operator.text)
        threshold = int(ctx.threshold.text)
        self.modes[-1].states[-1].transitions[-1].comparaisons.append(AnalogicComparison(sensor, threshold, operator))

    def enterDiscreteComparison(self, ctx:ArduinomlParser.DiscreteComparisonContext):
        trigger = ctx.trigger.text
        for brick in self.bricks:
            if brick.name == trigger:
                sensor = brick
                break
        else:
            raise RuntimeError(f'Unknown sensor {trigger}')
        value = SIGNAL(ctx.value.text)
        self.modes[-1].states[-1].transitions[-1].comparaisons.append(DiscreteComparison(sensor, value))

    def enterTemporalComparison(self, ctx:ArduinomlParser.TemporalComparisonContext):
        delay = int(ctx.delay.text)
        self.modes[-1].states[-1].transitions[-1].comparaisons.append(TemporalComparison(delay))

    def checkDebugOption(self, brick: Brick, ctx):
        if ctx.debug() is not None:
            self.monitor.addBrick((brick, ctx.debug().debug_type.text))
