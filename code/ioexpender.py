from smbus2 import SMBus,i2c_msg
from time import sleep

class PCF8575(object):
    WRITE_BIT              =0x00
    READ_BIT               =0x01

    def __init__(self,port=1,address=0x20) -> None:
        self.address=address
        # self.bus=smbus2.SMBus(port)
        self.port=port
        self.dataIn=0x0000
        self.dataOut=0xffff
        self.write16(self.dataOut)
        # self.buttonMask=0xffff
    def read16(self):
        with SMBus(self.port) as bus:
            msg=i2c_msg.read(self.address,2)
            bus.i2c_rdwr(msg)
            block=list(msg)
        # print(block)
        self.dataIn=block[0]|(block[1]<<8)
        return self.dataIn

    def read(self,pin):
        pin=int(pin)
        if(pin>15):
            raise Exception('pin is in [0,16)')
        self.read16()

        return (self.dataIn&(1<<pin))
    def readN(self,readlist):
        if(readlist>0xffff):
            raise Exception('readlist is in [0x0000,0xffff]')
        self.read16()
        return self.dataIn&readlist
    
    def write16(self,value):
        self.dataOut=value
        block=[value&0xff,value>>8]
        with SMBus(self.port) as bus:
            msg=i2c_msg.write(self.address,block)
            bus.i2c_rdwr(msg)
            # bus.write_i2c_block_data(self.address,0x00,block)
    def write(self,pin,value):
        if(pin>15):
            raise Exception('pin is in [0,16)')
        if(value==0):
            self.dataOut&=~(1<<pin)
        else:
            self.dataOut|=1<<pin
        self.write16(self.dataOut)
    def writeN(self,writelist,value):
        if(writelist>0xffff):
            raise Exception('writelist is in [0x0000,0xffff]')
        self.dataOut&=~writelist
        self.dataOut|=value
        self.write16(self.dataOut)



if(__name__=='__main__'):
    p=PCF8575(1,0x20)

    p.write16(0xfff0)
    ret=p.read16()
    print(bin(ret))
    sleep(2)
