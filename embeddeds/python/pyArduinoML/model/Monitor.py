from .Brick import Brick
from .DigitalSensor import DigitalSensor
from .AnalogSensor import AnalogSensor
from .Actuator import Actuator
import json

class Monitor():

    def __init__(self):
        self.bricks: list(tuple) = []
        # here we could also add mode and state

    def addBrick(self, brick: Brick):
        self.bricks.append(brick)

    def setup(self) -> str:
        return "\tSerial.begin(9600);"

    def loop(self) -> str:
        code = "Serial.write(\""
        data = {}
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
