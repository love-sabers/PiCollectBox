# 基于RaspberryPi5开发的建筑外立面损伤信息采集器

# 一.项目背景

本项目为“鉴微知筑”项目的子项目，主要负责解决主项目中面对的建筑外立面损伤信息采集问题。传统的信息采集方式主要依赖于无人机搭载高清摄像头对建筑外立面进行扫描，仅能收集到视觉信息，同时存在着大量的无用数据。由此，本项目组提出了利用真空吸盘实现的建筑外立面损伤信息采集爬墙机器人，其不仅可以收集实现精确的信息，同时可以通过敲击模块收集外立面的结构信息，通过红外模块收集外立面的温度信息，以达到对外立面的多维诊断。

“鉴微知筑”项目瞄准高层建筑外立面缺陷安全检测与数字化运维这个垂直细分领域，致力于打造一套面向高层建筑缺陷检测的数字诊疗与运维管理系统，做高层楼宇外立面病害探查的领军者。项目积极响应国家关于城市全域数字化转型、智慧城市建设等政策， 提供基于计算机视觉和深度学习的软硬件一体化解决方案，实现高效、准确的高层建筑外立面缺陷的数字诊疗与可视化运维管理，旨在解决目前高层建筑缺陷检测效率低下、人工排查不可靠、信息反馈延迟等痛点。

# 二.机器人架构

机器人主体主要有四个部分组成，分别是控制部分、运动部分、信息收集部分与能源部分。

控制部分主要由一台微型嵌入式计算机组成。

运动部分主要由两组大功率吸盘，三组高扭力步进电机，六组低扭力驱动轮以及配套的位姿感知模块组成。

信息收集部分主要由高清摄像头（视觉信息收集），敲击锤与收音设备（结构信息收集），红外摄像头（温度信息收集）组成。

能源部分主要由外接电源与内置电池组成。                                                                                                                                                                   

# 三.硬件配置

## 3.1 总体硬件关系

本部分仅展示本项目已经实现的视觉信息收集部分与基础I/O设备部分。

本项目目前仅支持基础的操作界面以及依赖高清摄像头的外立面损伤检测。

![架构图.drawio](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/%E6%9E%B6%E6%9E%84%E5%9B%BE.drawio.png)

## 3.2 核心开发板Raspberry Pi 5

本项目选择使用Raspberry Pi 5 作为核心开发板

Raspberry Pi 5 是最新一代的Raspberry Pi微型计算机，由Raspberry Pi Foundation开发。这款设备继承了前代产品的多功能性和高性价比，同时在性能和功能上都有显著提升。它配备了更强大的处理器，支持更高的运算速度，能更好地处理复杂的计算任务和多媒体处理。此外，Raspberry Pi 5 增加了对Wi-Fi 6和蓝牙5.2的支持，提供了更快更稳定的无线连接性能。在接口方面，它提供了全面的兼容性，包括多个USB端口、Gigabit Ethernet端口、以及对HDMI 2.1的支持，使其能够输出更高质量的视频信号。

![微信图片_20240618154012](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20240618154012.jpg)

## 3.3 端口扩展外设


### 3.3.1 PCA9548A 支持复位的低电压8通道I2C开关

PCA9548A 是一款支持复位功能的低电压8通道I2C开关，由德州仪器（Texas Instruments）生产。这款芯片主要用于扩展I2C总线通信，允许多个设备在同一总线上进行通信而不会出现地址冲突。

主要特点：

- **8个独立的I2C通道**：每个通道可以独立控制，使得多个I2C设备能够在同一主机上同时工作，各自独立操作，有效管理数据流和信号完整性。
- **低电压操作**：支持2.3V到5.5V的供电电压，适用于多种电子设备，特别是电源敏感的便携式设备。
- **复位功能**：集成硬件复位功能，可以通过一个外部信号重置开关状态，确保系统在电源波动或逻辑错误发生后能够快速恢复正常工作。
- **高带宽传输**：提供高速数据传输能力，适合需要高速数据处理和大量数据传输的应用。

PCA9548A适用于需要多个I2C设备同时操作的复杂系统，如多传感器系统、多屏显示设备和其他需要多I2C设备通信的应用。

本项目选择其作为I2C功能拓展，为后续的多传感器开发提供支持。

![微信图片_20240618155550](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20240618155550.jpg)

### 3.3.2 PCF8575 具有中断输出的远程16位I2C和SMBus I/O扩展器

PCF8575 是一款具有中断输出功能的远程16位I/O扩展器，它通过I2C和SMBus接口进行通信。该设备由NXP Semiconductors生产，主要用于扩展有限的微控制器I/O端口，在需要大量输入/输出操作的应用中特别有用。

主要特点：

- **16位双向I/O端口**：PCF8575提供16个独立的双向I/O端口，这些端口可以被配置为输入或输出，以满足不同的应用需求。
- **I2C接口**：支持标准（100kHz）、快速（400kHz）和高速（3.4MHz）I2C总线协议，确保与各种微控制器的兼容性。
- **中断输出**：具有中断输出功能，当任何输入端口状态改变时，它可以生成中断信号，通知主控制器进行相应处理，这有助于提高系统的响应速度和效率。
- **低电压操作**：工作电压范围从2.5V到5.5V，适合于多种电源环境，特别是电池供电的移动设备。
- **低功耗**：具有非常低的静态电流消耗，适合于电池供电的应用，可以延长电池寿命。

由于其灵活的配置和中断功能，PCF8575是一个高效的解决方案，用于增强微控制器的输入/输出功能，特别是在I/O资源有限的情况下。

本项目通过其扩展开发板有限的I/O资源。

![微信图片_20240618160018](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20240618160018.jpg)

## 3.4 基础I/O外设

### 3.4.1 SSD1315oled显示屏

SSD1315OLED显示屏驱动芯片常用于驱动小型到中型的OLED显示屏。这款芯片支持多种通信接口，如SPI和I2C，使其能够与各种微控制器或处理器轻松连接。SSD1315具备高度集成的显示控制功能，可以驱动高分辨率的OLED屏幕。此外，这款芯片还具有低功耗设计，适合于电池供电的移动设备使用。通过灵活的配置和编程，开发者可以轻松实现复杂的图形和动画效果，从而为最终产品提供高性能的视觉体验。

本项目选择该款显示屏作为机器人基本显示屏。

![微信图片_20240618154546](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20240618154546.jpg)

### 3.4.2 4x4矩阵键盘

4x4矩阵键盘是一种常用的输入设备，它包含16个按键，排列成4行4列的格局。这种键盘通常用于各种电子项目和设备，例如计算器、门禁系统、电话拨号盘等，因为它可以通过较少的I/O引脚与微控制器等电子设备连接，从而实现多个按键输入。矩阵键盘由16个按键组成，按键以4行4列的方式排列。每个按键在按下时会连接一个行线和一个列线。

本项目选择该键盘作为机器人基本输入。

![微信图片_20240618160401](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20240618160401.jpg)

## 3.5 视觉信息收集外设

### 3.5.1 USB48MP-QFZ 高清摄像头

USB48MP-QFZ高清摄像头是一款具备4800万像素的高分辨率USB接口摄像头，专为需要极高图像质量的应用设计。这种摄像头支持USB 3.0接口，确保快速、高效的数据传输，适合专业视频会议、高端直播、内容创作及工业视觉系统等场景。其主要特点包括即插即用功能，无需复杂安装即可使用，以及自动对焦、数字变焦和高动态范围（HDR）等增强功能，优化了在各种光照条件下的表现。

本项目通过其收集视觉信息

![微信图片_20240618161016](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20240618161016.jpg)



# 四.技术重点

## 4.1 端口扩展外设代码

### 4.1.1 PCA9548A 支持复位的低电压8通道I2C开关

PCA9548A采用IIC通讯方式进行通讯，对其的控制主要依赖对于其中内含的唯一一个8bit寄存器进行读写。

寄存器的每个bit与通道的关系如下：

<img src="./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/image-20240618215519960.png" alt="image-20240618215519960" style="zoom:80%;" />

寄存器的值与通道的通断关系如下：

![image-20240618215556331](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/image-20240618215556331.png)

简单来说，当对应bit为1时，通道导通，通道上的IIC设备接入IIC总线。例如，当B0为1时，通道0导通，通道0上的设备接入IIC总线。需要注意的是，当不同的通道接上相同地址的器件时，不应同时将通道导通，而应该在不同时间分别将通道导通。换言之，先导通其中一个通道进行通讯，通讯结束后，再导通另一个通道。这样的处理方式可以用来解决器件IIC地址冲突的问题。

对寄存器的读写，官方文档中通讯格式如下：

![image-20240618215206278](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/image-20240618215206278.png)

需要注意的是，因为整个芯片只有一个寄存器可供读写，所以**读写时不必向芯片传递寄存器地址。**

IIC通讯使用`smbus2`库实现。

为PCA9548A编写的控制类PCA9548A的代码见下：

```python
from smbus2 import SMBus,i2c_msg

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
    def __init__(self,port=1,address=0x70):
        #设定IIC端口与设备硬件地址
        self.address=address
        self.port=port
        with SMBus(self.port) as bus:
            msg=i2c_msg.write(self.address,[PCA9548A.CHANNEL_noselected])
            bus.i2c_rdwr(msg)
    def noselected(self):
        #软件复位
        with SMBus(self.port) as bus:
            msg=i2c_msg.write(self.address,[PCA9548A.CHANNEL_noselected])
            bus.i2c_rdwr(msg)
    def select_channel(self,channel):
        #选择通道
        with SMBus(self.port) as bus:
            msg=i2c_msg.write(self.address,[PCA9548A.CHANNEL[channel]])
            bus.i2c_rdwr(msg)
    def now_channel(self):
        #获取当前选择通道
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
```

### 4.1.2 PCF8575 具有中断输出的远程16位I2C和SMBus I/O扩展器

PCF8575采用IIC通讯方式进行通讯，对其的控制主要依赖对于其中内含的两个8bit寄存器进行读写。

寄存器的每个bit与引脚的关系如下：

![image-20240618221122997](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/image-20240618221122997.png)

简单来说，当对应bit为1时，尝试将IO上拉为正电压，当对应bit为0时将IO接地。若IO接地，则无法将IO上拉为正电压。

对寄存器的读写，官方文档中通讯格式如下：

![image-20240618221346616](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/image-20240618221346616.png)

![image-20240618221410373](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/image-20240618221410373.png)

需要注意的是，因为整个芯片只有一个寄存器可供读写，所以**读写时不必向芯片传递寄存器地址**，而传输的数据则始终规定为一个长度为16bit的数据。并且由于芯片的性质，在接受外界信号输入时要先将IO端口置为高电压。

IIC通讯使用`smbus2`库实现。

为PCF8575编写的控制类PCF8575的代码见下：

```python
from smbus2 import SMBus,i2c_msg

class PCF8575(object):
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
```

## 4.2 基础I/O外设代码

### 4.2.1 SSD1315oled显示屏

SSD1315与SSD1306虽然时是不同型号的芯片，但是二者仅仅在屏幕滚动上存在区别。为了方便实现，本部分直接调用了`luma.oled`库中的SSD1306的驱动。为了方便使用对其进行了二次封装以适配本项目的开发。

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306

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
    # o.rectangle((LEFT,YELLOW_TOP,RIGHT,BLUE_BOTTOM),inverse=1)
    # o.text((40,20),'HhiiH',inverse=1)
    o.clear(inverse=1)
```

### 4.2.2 4x4矩阵键盘

本项目采用的4x4矩阵键盘是最朴素的款式，不包含芯片，仅包含八个段子与十六个按钮，原理图见下：

![image-20240619140323722](./markdown-img/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.assets/image-20240619140323722.png)

其是由行线，列线，各四条线交叉形成的16个点组成的，按下按钮会导致对应的行线与列线导通。

基于这样的原理，我们可以先将行线所在端子拉高，列线所在端子接地，通过按下按钮后检测哪一个行线所在端子电平变为0，就可以判断按下按键所在的行。相同的方式也可以获取按键所在的列。

```python
from ioexpender import PCF8575

class keyboard_4plus4(object):

    def __init__(self,io:PCF8575,pinlist:list,keylist:list=[]):
        '''
        io:made with PCF8575
        pinlist:[C4,C3,C2,C1,R1,R2,R3,R4]
        '''
        self.io=io
        self.pre_status=0x0000

        self.col2pin=[pinlist[3],pinlist[2],pinlist[1],pinlist[0]]
        self.row2pin=[pinlist[4],pinlist[5],pinlist[6],pinlist[7]]

        self.USELIST=0x0000
        for i in pinlist:
            self.USELIST|=(1<<i)
            
        self.COLLIST=0x0000
        for i in self.col2pin:
            self.COLLIST|=(1<<i)

        self.ROWLIST=0x0000
        for i in self.row2pin:
            self.ROWLIST|=(1<<i)

        self.keylist=keylist

    def scan(self):
        self.io.writeN(self.USELIST,self.COLLIST)
        res=self.io.readN(self.USELIST)^self.COLLIST
        if(res):
            select_col=0
            for i in range(4):
                if res&(1<<self.col2pin[i]) :
                    select_col+=i+100        
            #如果有多列接通，则视作未按下
            if(select_col>=200 or select_col==0):
                return 0
        else:
            #未接通，无按钮被按下，恢复键盘初始状态
            self.pre_status=0x0000
            return 0
        
        self.io.writeN(self.USELIST,self.ROWLIST)
        res=self.io.readN(self.USELIST)^self.ROWLIST
        if(res):
            select_row=0
            for i in range(4):
                if res&(1<<self.row2pin[i]) :
                    select_row+=i+100
            if(select_row>=200 or select_row==0):
                return 0
        else:
            self.pre_status=0x0000
            return 0
        
        select_id=select_row*4+select_col-500
		
        #记录函数上次输出的值，使其仅在上升沿处返回按下的按钮
        if(self.pre_status&(1<<select_id)):
            return 0
        else :
            self.pre_status=1<<select_id
            return select_id+1

    def get_key(self):
        if(len(self.keylist)!=16):
            raise Exception("please set keylist correctly when init the keyboard")
        else:
            ret=self.scan()
            if(ret):
                return self.keylist[ret-1]
            else:
                return 0
        
if __name__=="__main__":
    io=PCF8575(port=1,address=0x20)
    keylist=['1','2','3','quit',
             '4','5','6','back',
             '7','8','9','pgup',
             '.','0','enter','pgdn']
    k=keyboard_4plus4(io,[0,1,2,3,4,5,6,7],keylist=keylist)
    while(1):
        ret=k.get_key()
        if(ret):
            print(ret)
                
```

## 4.3 视觉信息收集外设

### 4.3.1 USB48MP-QFZ 高清摄像头

该摄像头包含了易用的驱动程序，使用`linuxpy.vedio`库驱动摄像头。

示例程序如下：

```python
import cv2
import numpy as np
from linuxpy.video.device import Device,BufferType

print('test start')

def image_show(name,src):
    cv2.namedWindow(name,cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name,(1000,750))
    cv2.imshow(name,src)


cam=Device.from_id(0)
cam.open()
cam.set_format(BufferType.VIDEO_CAPTURE,4000,3000)
for frame in cam:
    image_np = np.frombuffer(frame.data, dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    image_show("cam",image)
    if cv2.waitKey(1) == ord('q'):
        break
cam.close()

print('test over')
```
