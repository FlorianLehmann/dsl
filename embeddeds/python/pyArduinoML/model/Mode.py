from pyArduinoML.model.NamedElement import NamedElement

class Mode(NamedElement):

    def __init__(self, name, transitions: tuple = (), states: tuple = ()):
        
        NamedElement.__init__(self, name)
        self.transitions: tuple = transitions
        self.states: tuple = states

    def setup(self):
        """
        Arduino code for the mode.

        :return: String
        """
        rtr = ""

        rtr += """void mode_%s() {
    functionPtr = mode_%s_state_%s;
    current_mode = String("%s");
    current_state = String("%s");
}

""" % (self.name, self.name, self.states[0].name, self.name, self.states[0].name)

        for state in self.states:
            rtr += "void mode_%s_state_%s() {\n" % (self.name, state.name)
            
            for transition in self.transitions:
                rtr += transition.setup(1, "mode_") + " else "

            rtr += "{\n"

            rtr += state.getContent(2, "mode_%s_state_" % self.name)

            rtr += "\n\t}"

            rtr += "\n}\n\n"
        

        return rtr
