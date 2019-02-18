from pyArduinoML.model.TemporalComparison import TemporalComparison
from pyArduinoML.model.Transition import Transition
from pyArduinoML.model.Mode import Mode
from pyArduinoML.model.State import State

transition1to2Mode = Transition('day', (TemporalComparison(5000),))
transition2to1Mode = Transition('night', (TemporalComparison(2000),))

state_1_day = State('1', (), (Transition('2', (TemporalComparison(3000),)),))
state_2_day = State('2', (), (Transition('1', (TemporalComparison(3000),)),))

mode_day = Mode('day', (transition2to1Mode,), (state_1_day, state_2_day,))

print(mode_day.setup())