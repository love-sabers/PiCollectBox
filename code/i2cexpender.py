from smbus2 import SMBus,i2c_msg
from oled import oled
from time import sleep

class PCA9548A(object):
    CHANNEL_noselected     =0x00
    CHANNEL                =(0x01,
                             0x02,
                             0x04,
                             0x08,
                             0x10,
                             0x20,
                             0x40,
                             0x80)
    def __init__(self,port=1,address=0x70) -> None:
        self.address=address
        self.port=port
        # self.bus=smbus2.SMBus(port)
        with SMBus(self.port) as bus:
            msg=i2c_msg.write(self.address,[PCA9548A.CHANNEL_noselected])
            bus.i2c_rdwr(msg)
    def noselected(self):
        with SMBus(self.port) as bus:
            msg=i2c_msg.write(self.address,[PCA9548A.CHANNEL_noselected])
            bus.i2c_rdwr(msg)
    def select_channel(self,channel):
        with SMBus(self.port) as bus:
            msg=i2c_msg.write(self.address,[PCA9548A.CHANNEL[channel]])
            bus.i2c_rdwr(msg)
    def now_channel(self):
        with SMBus(self.port) as bus:
            msg=i2c_msg.read(self.address,1)
            bus.i2c_rdwr(msg)
            ret=list(msg)[0]
        if(ret==0):
            return None
        for i in range(8):
            if(ret==PCA9548A.CHANNEL[i]):
                return i


if(__name__=='__main__'):
    s=PCA9548A(1,0x70)
    s.select_channel(3)
    print(s.now_channel())
    # o=oled(1,0x3c)
    # o.text((20,20),'hhh')
    # sleep(2)
    # o.text((20,20),'aaa',)
    # sleep(10)