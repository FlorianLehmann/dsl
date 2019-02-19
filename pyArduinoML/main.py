from pyArduinoML.model.TemporalComparison import TemporalComparison
from pyArduinoML.model.Transition import Transition
from pyArduinoML.model.Mode import Mode
from pyArduinoML.model.State import State

transition1to2Mode = Transition('day', (TemporalComparison(5000),))
transition2to1Mode = Transition('night', (TemporalComparison(2000),))

state_1_day = State('1', (), (Transition('2', (TemporalComparison(9000),)),))
state_2_day = State('2', (), (Transition('1', (TemporalComparison(3000),)),))

state_1_night = State('1_bis', (), (Transition('2_bis', (TemporalComparison(500),)),))
state_2_night = State('2_bis', (), (Transition('3', (TemporalComparison(380),)),))
state_3_night = State('3', (), (Transition('1_bis', (TemporalComparison(50),)), Transition('2_bis', (TemporalComparison(59700),)),))

mode_day = Mode('day', (transition2to1Mode,), (state_1_day, state_2_day,))
mode_night = Mode('night', (transition1to2Mode,), (state_1_night, state_2_night,state_3_night,))

print(mode_day.setup())
print(mode_night.setup())