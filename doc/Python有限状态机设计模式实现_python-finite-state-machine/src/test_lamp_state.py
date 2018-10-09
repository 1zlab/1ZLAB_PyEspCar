from lamp_state import *

lamp_state = LampOff()

print(lamp_state)

lamp_state.switch(LampLightMiddle)
lamp_state.switch(LampLightBright)
lamp_state.switch(LampLightMiddle)