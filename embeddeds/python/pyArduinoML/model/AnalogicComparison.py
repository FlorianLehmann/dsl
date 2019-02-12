from pyArduinoML.model.Comparison import Comparison

from .SIGNAL import value
from .Sensor import Sensor
import AnalogicOperator

class AnalogicComparison(Comparison) :

    def __init__(self, sensor: Sensor, value: int, operator: AnalogicOperator):
        self.sensor: Sensor = sensor
        self.value: int = value
        self.operator: AnalogicOperator = operator

    def setup(self):
        return "analogRead(%s) %s %s" % (self.sensor.name, self.operator, value(self.value))
