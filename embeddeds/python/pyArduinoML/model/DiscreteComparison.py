from pyArduinoML.model.Comparison import Comparison

class DiscreteComparison(Comparison) :

    def __init__(self, sensor, value):
        self.sensor = sensor
        self.value = value

    def setup(self):
        return "digitalRead(%s) == %s" % (self.sensor.name, SIGNAL.value(self.value)
