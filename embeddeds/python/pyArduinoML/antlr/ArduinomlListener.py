# Generated from pyArduinoML/antlr/Arduinoml.g4 by ANTLR 4.6
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ArduinomlParser import ArduinomlParser
else:
    from ArduinomlParser import ArduinomlParser

# This class defines a complete listener for a parse tree produced by ArduinomlParser.
class ArduinomlListener(ParseTreeListener):

    # Enter a parse tree produced by ArduinomlParser#root.
    def enterRoot(self, ctx:ArduinomlParser.RootContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#root.
    def exitRoot(self, ctx:ArduinomlParser.RootContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#declaration.
    def enterDeclaration(self, ctx:ArduinomlParser.DeclarationContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#declaration.
    def exitDeclaration(self, ctx:ArduinomlParser.DeclarationContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#bricks.
    def enterBricks(self, ctx:ArduinomlParser.BricksContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#bricks.
    def exitBricks(self, ctx:ArduinomlParser.BricksContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#sensor.
    def enterSensor(self, ctx:ArduinomlParser.SensorContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#sensor.
    def exitSensor(self, ctx:ArduinomlParser.SensorContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#actuator.
    def enterActuator(self, ctx:ArduinomlParser.ActuatorContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#actuator.
    def exitActuator(self, ctx:ArduinomlParser.ActuatorContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#location.
    def enterLocation(self, ctx:ArduinomlParser.LocationContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#location.
    def exitLocation(self, ctx:ArduinomlParser.LocationContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#debug.
    def enterDebug(self, ctx:ArduinomlParser.DebugContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#debug.
    def exitDebug(self, ctx:ArduinomlParser.DebugContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#modes.
    def enterModes(self, ctx:ArduinomlParser.ModesContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#modes.
    def exitModes(self, ctx:ArduinomlParser.ModesContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#initialMode.
    def enterInitialMode(self, ctx:ArduinomlParser.InitialModeContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#initialMode.
    def exitInitialMode(self, ctx:ArduinomlParser.InitialModeContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#customMode.
    def enterCustomMode(self, ctx:ArduinomlParser.CustomModeContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#customMode.
    def exitCustomMode(self, ctx:ArduinomlParser.CustomModeContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#modeTransition.
    def enterModeTransition(self, ctx:ArduinomlParser.ModeTransitionContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#modeTransition.
    def exitModeTransition(self, ctx:ArduinomlParser.ModeTransitionContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#states.
    def enterStates(self, ctx:ArduinomlParser.StatesContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#states.
    def exitStates(self, ctx:ArduinomlParser.StatesContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#initialState.
    def enterInitialState(self, ctx:ArduinomlParser.InitialStateContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#initialState.
    def exitInitialState(self, ctx:ArduinomlParser.InitialStateContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#customState.
    def enterCustomState(self, ctx:ArduinomlParser.CustomStateContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#customState.
    def exitCustomState(self, ctx:ArduinomlParser.CustomStateContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#action.
    def enterAction(self, ctx:ArduinomlParser.ActionContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#action.
    def exitAction(self, ctx:ArduinomlParser.ActionContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#stateTransition.
    def enterStateTransition(self, ctx:ArduinomlParser.StateTransitionContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#stateTransition.
    def exitStateTransition(self, ctx:ArduinomlParser.StateTransitionContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#expression.
    def enterExpression(self, ctx:ArduinomlParser.ExpressionContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#expression.
    def exitExpression(self, ctx:ArduinomlParser.ExpressionContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#comparison.
    def enterComparison(self, ctx:ArduinomlParser.ComparisonContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#comparison.
    def exitComparison(self, ctx:ArduinomlParser.ComparisonContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#analogicComparison.
    def enterAnalogicComparison(self, ctx:ArduinomlParser.AnalogicComparisonContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#analogicComparison.
    def exitAnalogicComparison(self, ctx:ArduinomlParser.AnalogicComparisonContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#discreteComparison.
    def enterDiscreteComparison(self, ctx:ArduinomlParser.DiscreteComparisonContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#discreteComparison.
    def exitDiscreteComparison(self, ctx:ArduinomlParser.DiscreteComparisonContext):
        pass


    # Enter a parse tree produced by ArduinomlParser#temporalComparison.
    def enterTemporalComparison(self, ctx:ArduinomlParser.TemporalComparisonContext):
        pass

    # Exit a parse tree produced by ArduinomlParser#temporalComparison.
    def exitTemporalComparison(self, ctx:ArduinomlParser.TemporalComparisonContext):
        pass


