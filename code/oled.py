#!/usr/bin/python3
# -*- coding: utf-8 -*-
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
from time import sleep
"""
SSD3515 luma 驱动库测试程序
功能：显示 hello world 和矩形外框持续10秒
"""



def color_config(func):
    def wrapper(self, *args, **kwargs):
        inverse = kwargs.get('inverse', 0)  # 获取 inverse 参数，默认为 0
        if inverse:
            foreground = 'black'
            background = 'white'
        else:
            foreground = 'white'
            background = 'black'
        
        # 替换或添加 foreground 和 background 参数
        kwargs['foreground'] = foreground
        kwargs['background'] = background
        
        # 移除 inverse 参数，因为它不再需要被传递到原始函数
        if 'inverse' in kwargs:
            del kwargs['inverse']
        
        # 调用原始函数，传递修改后的参数
        return func(self, *args, **kwargs)
    return wrapper



class SSD3515(object):
    LEFT=0
    RIGHT=127
    TOP=0
    BOTTOM=63
    YELLOW_TOP=0
    YELLOW_BOTTOM=15
    BLUE_TOP=16
    BLUE_BOTTOM=63
    def __init__(self,port=1,address=0x3c) -> None:
        # 初始化端口
        serial = i2c(port=port, address=address)
        # 初始化设备，这里改ssd1306, ssd1325, ssd1331, sh1106
        self.device = ssd1306(serial)
        self.canvas = canvas(self.device)
        self.drawContinuously=0

    def openContinuously(self):
        self.drawContinuously=1
        self.canvas.__enter__()
    
    def closeContinuesly(self):
        self.drawContinuously=0
        self.canvas.__exit__(None,None,None)

    @color_config
    def clear(self,foreground,background,inverse=0):
        if(self.drawContinuously):
            self.canvas.draw.rectangle((SSD3515.LEFT,SSD3515.TOP,SSD3515.RIGHT,SSD3515.BOTTOM), outline=foreground, fill=background,width=0)
        else:         
            with self.canvas as draw:
                draw.rectangle((SSD3515.LEFT,SSD3515.TOP,SSD3515.RIGHT,SSD3515.BOTTOM), outline=foreground, fill=background,width=0)

    @color_config    
    def rectangle(self,pos,foreground,background,width=1,inverse=0):
        if(self.drawContinuously):
            self.canvas.draw.rectangle(pos, outline=foreground, fill=background,width=width)
        else:         
            with self.canvas as draw:
                draw.rectangle(pos, outline=foreground, fill=background,width=width)
                
    
    @color_config
    def text(self,pos,str,foreground,background,inverse=0):
        if(self.drawContinuously):
            self.canvas.draw.rectangle((SSD3515.LEFT,pos[1]+1,SSD3515.RIGHT,pos[1]+10),outline=background,fill=background)
            self.canvas.draw.text(pos, str, fill=foreground)
        else:
            with self.canvas as draw:   
                draw.rectangle((SSD3515.LEFT,pos[1]+1,SSD3515.RIGHT,pos[1]+10),outline=background,fill=background)
                draw.text(pos, str, fill=foreground)


if(__name__=='__main__'):
    # 调用显示函数
    o=SSD3515(port=1,address=0x3C)
    # canvas(o.device).rectangle((LEFT,YELLOW_TOP,RIGHT,BLUE_BOTTOM),foreground="blue", background="black")
    # o.rectangle((LEFT,YELLOW_TOP,RIGHT,BLUE_BOTTOM),inverse=1)
    o.text((40,20),'HhiiH',inverse=1)
    o.clear(inverse=1)

    # __version__ = 1.0
    # # 初始化端口
    # serial = i2c(port=1, address=0x3C)
    # # 初始化设备，这里改ssd1306, ssd1325, ssd1331, sh1106
    # device = ssd1306(serial)
    # print("当前版本：", __version__)
    # # 调用显示函数
    # with canvas(device) as draw:
    #  draw.rectangle(device.bounding_box, foreground="white", background="black")
    #  draw.text((30, 20), "Hello World", background="white")

    # while(1):
        # pass    
    # 延时显示10s
    sleep(2)
