__author__ = 'pascalpoizat'

class Transition :
    """
    A transition between two states.
    """

    def __init__(self, nextelement: 'State', comparisons: tuple = ()):
        self.comparisons = comparisons
        self.nextelement = nextelement

    def setup(self, tabNb = 1, complementary = ""):
        res = "\t"*tabNb + "if ("
        
        for comparison in self.comparisons:
            res += comparison.setup() + " && "
        
        res += "guard) {\n" + "\t"*(tabNb+1) + "time = millis(); functionPtr = %sstate_%s;\n" % (complementary, self.nextelement) + "\t"*tabNb +"}"

        return res
