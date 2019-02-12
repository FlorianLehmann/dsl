from pyArduinoML.model.Comparison import Comparison
from .SIGNAL import SIGNAL

class DiscreteComparison(Comparison) :

    def __init__(self, sensor: str, value: SIGNAL):
        self.sensor: str = sensor
        self.value: SIGNAL = value

    def setup(self):
        return "digitalRead(%s) == %s" % (self.sensor.name, self.value.__str__())
