from machine import I2C
import struct

PORTA = (21,22)
PORTC = (17,16)
M_BUS = PORTA

bus_0 = None
bus_1 = None
bus_other = None

def get(port):
    global bus_0, bus_1, bus_other
    if port == PORTA or port == M_BUS:
        if bus_0 == None:
            bus_0 = I2C(id=0, sda=port[0], scl=port[1])
        return bus_0
    elif port == PORTC:
        if bus_1 == None:
            bus_1 = I2C(id=1, sda=port[0], scl=port[1])
        return bus_1
    else:
        if bus_1 == None:
            if bus_other == None:
                bus_other = I2C(id=1, sda=port[0], scl=port[1])
                return bus_other
            else:
                return bus_other
        else:
            raise OSError('I2C bus not support 3')

class easyI2C():
    def __init__(self, port, addr):
        self.i2c = get(port)
        self.addr = addr

    def write_u8(self, reg, data):
        buf = bytearray(1)
        buf[0] = data
        self.i2c.writeto_mem(self.addr, reg, buf)

    def write_u16(self, reg, data, byteorder='big'):
        buf = bytearray(2)
        encode = '<h' if byteorder == 'little' else '>h'
        struct.pack_into(encode, buf, 0, data)
        self.i2c.writeto_mem(self.addr, reg, buf)
    
    def read_u8(self, reg):
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]
    
    def read_u16(self, reg, byteorder='big'):
        buf = bytearray(2)
        self.i2c.readfrom_mem_into(self.addr, reg, buf)
        encode = '<h' if byteorder == 'little' else '>h'
        return struct.unpack(encode, buf)[0]
    
    def read(self, num):
        return self.i2c.readfrom(self.addr, num)

    def read_reg(self, reg, num):
        return self.i2c.readfrom_mem(self.addr, reg, num)

    def scan(self):
        return self.i2c.scan()
    
    def available(self):
        return self.i2c.is_ready(self.addr)
            
