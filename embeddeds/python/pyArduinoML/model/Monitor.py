from .Brick import Brick
from .DigitalSensor import DigitalSensor
from .AnalogSensor import AnalogSensor
from .Actuator import Actuator

class Monitor():

    def __init__(self):
        self.bricks: list = []
        # here we could also add mode and state

    def addBrick(self, brick: Brick):
        self.bricks.append(brick)

    def setup(self) -> str:
        return "\tSerial.begin(9600);"

    def loop(self) -> str:
        code = "Serial.write(\""
        
        code += """{ \\
                \\"StateMachine\\": \\"<dotfile>\\",\\"Bricks\\" : { \\
                    Sensor : ["""

        for i, brick in enumerate(self.bricks):
            if i > 0:
                code += ","

            if isinstance(brick, DigitalSensor):
                code += "DigitalSensor { %s : digitalRead(%s) }" % (brick.name, brick.pin)
            elif isinstance(brick, AnalogSensor):
                pass

        code += "], Actuator : [ "

        for brick in self.bricks:
            if isinstance(brick, Actuator):
                code += "{ %s : %s }" % (brick.name, brick.value)
            
        
        code += "]}}\");"

        return code
