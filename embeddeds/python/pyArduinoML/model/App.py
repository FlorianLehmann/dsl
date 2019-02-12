__author__ = 'pascalpoizat'

from pyArduinoML.model.NamedElement import NamedElement


class App(NamedElement):
    """
    Application built over bricks.

    """

    def __init__(self, name: str, bricks: tuple=(), states: tuple=()):
        """
        Constructor.

        :param name: String, the name of the application
        :param bricks: List[Brick], bricks over which the application operates
        :param states: List[State], states of the application with the first one being the initial state
        :return:
        """
        NamedElement.__init__(self, name)
        self.bricks: tuple = bricks
        self.states: tuple = states

    def __repr__(self):
        """
        External representation: Arduino program

        :return: String
        """

        rtr = """// generated by ArduinoML

%s

void setup() {
%s
}

int state = LOW; int prev = HIGH;
long time = 0; long debounce = 200;

%s
void loop() { state_%s(); }""" % ("\n".join(map(lambda b: b.declare(), self.bricks)),
                                  "\n".join(map(lambda b: b.setup(), self.bricks)),
                                  "\n".join(map(lambda s: s.setup(), self.states)),
                                  self.states[0].name)
        return rtr
