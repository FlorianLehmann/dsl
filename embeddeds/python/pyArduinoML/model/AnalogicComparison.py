from pyArduinoML.model.Comparison import Comparison


class AnalogicComparison(Comparison) :

    def __init__(self, sensor, value, operator):
        self.sensor = sensor
        self.value = value
        self.operator = operator

    def setup(self):
        return "analogRead(%s) %s %s" % (self.sensor.name, AnalogicComparison.value(self.operator), SIGNAL.value(self.value))
