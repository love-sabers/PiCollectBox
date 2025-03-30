from time import sleep
from keyboard import keyboard_4plus4
from ioexpender import PCF8575
from oled import SSD3515
from datetime import datetime


class Menu:
    ITEMS_PER_PAGE=3
    def __init__(self,keyboard:keyboard_4plus4,oled:SSD3515,menu_items):
        self.keyboard=keyboard
        self.oled=oled
        self.now_selected=0
        self.menu_items=menu_items 
        self.menu_len=len(menu_items)


    def condition_display(self):
        now=datetime.now()
        current_hour_minute = now.strftime("%H:%M")
        self.oled.text((0,0),f"time:{current_hour_minute}",inverse=1)

    def render(self):
        # self.oled.clear()
        self.condition_display()
        page=(int)(self.now_selected/Menu.ITEMS_PER_PAGE)
        self.oled.openContinuously()
        for i in range(Menu.ITEMS_PER_PAGE):
            id=page*Menu.ITEMS_PER_PAGE+i
            self.oled.text((SSD3515.LEFT,SSD3515.BLUE_TOP+i*16),self.menu_items[id],inverse=(id==self.now_selected))
        self.oled.closeContinuesly()

    def get_option(self):
        self.oled.clear()
        while(1):
            key=self.keyboard.get_key()
            if(key):
                print(key)
                if(key.isdigit()):
                    self.now_selected=min(self.menu_len,int(key)-1)
                elif(key=='enter'):
                    return self.now_selected+1
                elif(key=='pgup'):
                    self.now_selected=max(0,self.now_selected-1)
                elif(key=='pgdn'):
                    self.now_selected=min(self.menu_len-1,self.now_selected+1)
                elif(key=='quit'):
                    return 0

            self.render()
            sleep(0.01)
            

def main():
    oled=SSD3515(port=1,address=0x3c)
    io=PCF8575(port=1,address=0x20)
    keylist=['1','2','3','quit',
             '4','5','6','back',
             '7','8','9','pgup',
             '.','0','enter','pgdn']
    keyboard=keyboard_4plus4(io,[0,1,2,3,4,5,6,7],keylist)
    menu=Menu(keyboard,oled,['start','setting','option3','option4','option5','option6'])
    while(1):
        option=menu.get_option()
        if(option):
            print(option)
        else:
            break

if __name__ == '__main__':
    main()