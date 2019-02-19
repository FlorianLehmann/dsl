from .Brick import Brick
from .DigitalSensor import DigitalSensor
from .AnalogSensor import AnalogSensor
from .Actuator import Actuator
import json

def _mode_to_json(mode):
    return {
        "name": mode.name,
        "states": [_state_to_json(state) for state in mode.states],
        "transitions": [_transition_to_json(transition) for transition in mode.transitions]
    }


def _state_to_json(state):
    return {
        "name": state.name,
        "transitions": [_transition_to_json(transition) for transition in state.transitions]
    }


def _transition_to_json(transition):
    return {
        "nextelement": transition.nextelement.name
    }


class Monitor():

    def __init__(self, name):
        self.name = name
        self.bricks: list(tuple) = []
        self.modes = []
        self.showStateMachine: bool = False

    def addBrick(self, brick: Brick):
        self.bricks.append(brick)
    
    def addMode(self, mode):
        self.modes.append(mode)

    def setup(self) -> str:
        return "\tSerial.begin(9600);"

    def loop(self) -> str:
        code = "Serial.write(\""
        data = {}
        data['name'] = self.name
        if self.showStateMachine:
            data['StateMachine'] = str([_mode_to_json(mode) for mode in self.modes])
        data['Bricks'] = []

        stack = []
        
        for i, (brick, mode) in enumerate(self.bricks):
            if isinstance(brick, DigitalSensor):
                str_brick = { "type": "DigitalSensor", brick.name: "%", "mode": mode }
                stack.append("digitalRead(" + str(brick.pin) +")")
            elif isinstance(brick, AnalogSensor):
                pass
            elif isinstance(brick, Actuator):
                str_brick = { "type": "Actuator", brick.name: "%", "mode": mode }
                stack.append("digitalReadOutputPin(" + str(brick.pin) + ")")
            data['Bricks'].append(str_brick)

        code += json.dumps(data).replace('\"', '\\"')
        code += "\");"

        for i in  stack:
            code = code.replace("%", '"); Serial.write(' + str(i) + '); Serial.write("', 1)

        return code
