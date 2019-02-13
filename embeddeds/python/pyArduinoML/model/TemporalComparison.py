from pyArduinoML.model.Comparison import Comparison

class TemporalComparison(Comparison) :

    def __init__(self, time):
        self.time = time

    def setup(self):
        return "millis() - time > " + str(self.time)
