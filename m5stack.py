import display, m5base
import machine, binascii, os
from button import Btn, BtnChild
from micropython import const
from lib.speak import Speaker
from units._rgb_multi import Rgb_multi

__VERSION__ = m5base.get_version()

_BUTTON_A_PIN = const(39)
_BUTTON_B_PIN = const(38)
_BUTTON_C_PIN = const(37)

_sdCardState = False

def sd_mount():
    import os
    os.sdconfig(os.SDMODE_SPI, clk=18, mosi=23, miso=19, cs=4, maxspeed=40)
    os.mountsd()

def sd_umount():
    try:
        os.umountsd()
    except:
        pass

def get_sd_state():
    return _sdCardState

def hwDeinit():
    rgb.setColorAll(0x000000)
    rgb.setBrightness(40)

def btnText(number, message):
    x_pos = 0
    if number == 'A':
        x_pos = 62
    elif number == 'B':
        x_pos = 159
    elif number == 'C':
        x_pos = 253
    lcd.text(x_pos - int(lcd.textWidth(message) / 2), 235 - lcd.fontSize()[1], message)


# ============================================================================================

lcd = display.TFT()
lcd.init(lcd.M5STACK, width=240, height=320, speed=40000000, rst_pin=33, 
         miso=19, mosi=23, clk=18, cs=14, dc=27, bgr=True,invrot=3, 
         expwm=machine.PWM(32, freq=38000, duty=0, timer=1))
lcd.setBrightness(30)

btn = Btn()
btnA = btn.attach(_BUTTON_A_PIN)
btnB = btn.attach(_BUTTON_B_PIN)
btnC = btn.attach(_BUTTON_C_PIN)

speaker = Speaker()

from lib import time_ex
timEx = time_ex.TimerEx()

rgb = Rgb_multi((15,), 10)
rgb.setColorAll(0x000000)
rgb.setBrightness(40)

try:
    sd_mount()
    _sdCardState = True
except:
    _sdCardState = False
    
node_id = binascii.hexlify(machine.unique_id()).decode('utf-8')

print("[ M5 ] init sd card {}".format('OK' if _sdCardState else 'Fail'))
print("[ M5 ] node id:{}".format(node_id))
