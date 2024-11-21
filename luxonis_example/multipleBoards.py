import os
from adafruit_blinka.microcontroller.rp2040_u2if.pin import Pin
from adafruit_blinka.microcontroller.rp2040_u2if.rp2040_u2if import RP2040_u2if
from specific_board import init_specific_board, display_connected_rp2040, RP2040_u2if_init
from time import sleep

os.environ["BLINKA_U2IF"]="1"


display_connected_rp2040()


import time
import adafruit_apds9960.apds9960
# Initialize I2C using u2if's I2C interface
#board2=init_specific_board(0xE6636825930C7C23)

#This class is more low level, used mostly for GPIO manipulation.
def press_button(button):
    print("Pressing button")
    button.value = False
    # If delay is too small button will not siwtch. With delay of 3 seconds, this worked pretty much 100% od the time
    sleep(3)
    button.value = True
    #If you retry multiple times, you need this delay.
    sleep(2)


def toogle_to_correct(led, button, wanted_state):
    for i in range(5):
        if bool(int(wanted_state)) == led.value:
            return True
        else:
            press_button(button)

    raise Exception("Toogle unsuccessful, didnt change states")



# This is high level adafruit class used for I2C.
# Do not import the board class if you are using multiple rp2040  without this method as you cant control the serial of the board
board1, busio1, digitalio=init_specific_board("0xE6636825930C7C23")
i2c = busio1.I2C(board1.GP5, board1.GP4)  # SCL, SDA for default I2C1
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

led = digitalio.DigitalInOut(board1.GP1)  # Replace GP15 with your desired pin
led.direction = digitalio.Direction.INPUT

button = digitalio.DigitalInOut(board1.GP0)  # Replace GP15 with your desired pin
button.direction = digitalio.Direction.OUTPUT
# Enable color sensing
sensor.enable_color = True

print("INIT GPIO")
# Main loop to read RGB data
print("Inside main loop")
r, g, b, c = 1,1,1,1
state=True
while True:
    r, g, b, c = sensor.color_data  # Red, Green, Blue, and Clear channel data
    print(f"Red: {r}, Green: {g}, Blue: {b}, Clear: {c}")
    if r > g and r > b:
        print("RED")
    if g > r and g > b:
        print("GREEN")
    if b > g and b > r:
        print("BLUE")
    #toogle_to_correct(led, button, state)
    #state=not state
