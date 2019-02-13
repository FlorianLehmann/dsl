__author__ = 'pascalpoizat'

class Transition :
    """
    A transition between two states.
    """

    def __init__(self, nextstate: 'State', comparisons: tuple = ()):
        self.comparisons = comparisons
        self.nextstate = nextstate

    def setup(self):
        res = "\tif ("
        
        for comparison in self.comparisons:
            res += comparison.setup() + " && "
        
        res += "guard) {\n\t\ttime = millis(); functionPtr = state_%s;\n\t}" % self.nextstate.name

        return res
