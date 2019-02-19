from .Brick import Brick
from .DigitalSensor import DigitalSensor
from .AnalogSensor import AnalogSensor
from .Actuator import Actuator
import json

class Monitor():

    def __init__(self):
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
        if self.showStateMachine:
            data['StateMachine'] = '<dotfile>'
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
