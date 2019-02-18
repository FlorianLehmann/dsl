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
        
        for i, (brick, mode) in enumerate(self.bricks):
            if isinstance(brick, DigitalSensor):
                brick = { "type": "DigitalSensor", brick.name: "digitalRead(" + str(brick.pin) +")", "mode": mode }
            elif isinstance(brick, AnalogSensor):
                pass
            elif isinstance(brick, Actuator):
                brick = { "type": "Actuator", brick.name: brick.pin, "mode": mode }
            data['Bricks'].append(brick)
        
        code += json.dumps(data).replace('\"', '\\"')
        code += "\");"

        return code
