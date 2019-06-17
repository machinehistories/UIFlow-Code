from machine import ADC
from machine import PWM
from machine import Pin

_adc_map ={}
_pwm_map = {}
_io_map = {}

def analogRead(pin):
    if pin not in _adc_map.keys():
        try:
            _adc_map[pin] = ADC(pin)
            _adc_map[pin].atten(ADC.ATTN_11DB)
            _adc_map[pin].width(ADC.WIDTH_12BIT)
        except:
            return 0

    data = _adc_map[pin].read()
    ad_data = int(data * 1024 / 3300)
    return ad_data

def analogWrite(pin, duty):
    if pin not in _pwm_map.keys():
        try:
            _pwm_map[pin] = PWM(pin, duty=duty, timer=1)
        except:
            pass
    else:
        _pwm_map[pin].duty(duty)
    
def digitalWrite(pin, value):
    if str(pin) not in _io_map.keys():
        _io_map[pin] = Pin(pin, mode=Pin.INOUT, pull=Pin.PULL_UP)
    _io_map[pin].value(value)
    
def digitalRead(pin):
    if pin not in _io_map.keys():
        if pin > 34:
            _io_map[pin] = Pin(pin, mode=Pin.IN, pull=Pin.PULL_UP)
        else:
            _io_map[pin] = Pin(pin, mode=Pin.INOUT, pull=Pin.PULL_UP)
    return _io_map[pin].value()

def toggleIO(pin):
    digitalWrite(pin, 1 - digitalRead(pin))

def map_value(value, input_min, input_max, aims_min, aims_max):
    value = min(max(input_min, value), input_max)
    value_deal = (value - input_min) * (aims_max - aims_min) / (input_max - input_min) + aims_min
    return round(value_deal, 2)

def _deinitIO():
    global _adc_map, _pwm_map, _io_map
    
    for i in _adc_map.values():
        i.deinit()
    
    for i in _pwm_map.values():
        i.deinit()
    
    for i in _io_map.values():
        i.deinit()

    _adc_map, _pwm_map, _io_map = {}, {}, {}
