from time import sleep
from keyboard import keyboard_4plus4
from ioexpender import PCF8575
from oled import SSD3515
from menu import Menu
from video_detect import detect_cracks
from video_collect import collect_data

def main():
    oled=SSD3515(port=1,address=0x3c)
    io=PCF8575(port=1,address=0x20)
    keylist=['1','2','3','quit',
             '4','5','6','back',
             '7','8','9','pgup',
             '.','0','enter','pgdn']
    keyboard=keyboard_4plus4(io,[0,1,2,3,4,5,6,7],keylist)
    menu=Menu(keyboard,oled,['collect','detection','setting','option4','option5','option6'])
    while(1):
        option=menu.get_option()
        if(option):
            print(option)
            if(option==1):
                collect_data(keyboard,oled)
            elif(option==2):
                detect_cracks(keyboard,oled)
        else:
            break

if __name__ == '__main__':
    main()