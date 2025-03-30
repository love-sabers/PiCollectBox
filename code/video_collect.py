import cv2
import os
import datetime
import numpy as np
# from linuxpy.video.device import Device,BufferType
from v4l2py.device import Device, BufferType
from keyboard import keyboard_4plus4
from oled import SSD3515

def image_show(name,src):
    cv2.namedWindow(name,cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name,(1000,750))
    cv2.imshow(name,src)

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
       


def collect_data(keyboard:keyboard_4plus4,oled:SSD3515,filename=None,collect_rate=30):
    
    oled.clear()
    oled.text((30,20),'collect start')

    cam=Device.from_id(0)
    cam.open()
    cam.set_format(BufferType.VIDEO_CAPTURE,4000,3000)

    if filename==None:
        current_time = datetime.datetime.now()
        time_str = current_time.strftime("%Y%m%d_%H%M%S")
        filename = f"video_collect_{time_str}"

    filepath='video_data/'+filename
    make_dir(filepath)

    i=0
    for frame in cam:
        image_np = np.frombuffer(frame.data, dtype=np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        image_show("cam",image)
        if(i%30==0):
            cv2.imwrite(filepath+'/'+filename+f'_{int(i/30):05d}.jpg',image)
        i=i+1    

        key=keyboard.get_key()
        if(key=='back'):
            break
        # 按 'q' 键退出
        if cv2.waitKey(1) == ord('q'):
            break
    cam.close()
    cv2.destroyAllWindows()

if __name__=='__main__':
    print('test start')
    collect_data()
    print('test over')