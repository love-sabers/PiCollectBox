import cv2
import numpy as np
from ultralytics import YOLO
from predict import pred_frame
from PIL import Image
from keyboard import keyboard_4plus4
from oled import SSD3515

def detect_cracks(keyboard:keyboard_4plus4,oled:SSD3515):

    oled.clear()
    oled.text((30,20),'detect start')

    #set camera
    cap = cv2.VideoCapture(0)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("can't open camera")
        exit()

    desired_width = 640
    desired_height = 480
    desired_fps = 10
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,desired_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,desired_height)  
    cap.set(cv2.CAP_PROP_FPS,desired_fps)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f"width: {width}px, height: {height}px,fps: {fps}")

    #set model
    model = YOLO("runs/segment/419-all/weights/blockonly.pt")  # load a custom model
    resPath='result/'
    srcPath='source/'


    # 循环以帧方式读取摄像头图像
    id=0
    while 1:
        # 逐帧捕捉
        id=id+1
        ret, frame = cap.read()
        
        # 如果正确读取帧，ret为True
        if not ret:
            print("无法读取摄像头帧，请检查摄像头连接状态")
            break


    
        # 将 BGR 转换为 RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 将 NumPy 数组转换为 PIL 图像
        frame_pil = Image.fromarray(frame_rgb)

        result=pred_frame(id,frame_pil,model,resPath)
        resimg=result.plot()


        # if resimg.mode != 'RGB':
        #     resimg = resimg.convert('RGB')
        # # 将 PIL 图像转换为 NumPy 数组
        # result_np = np.array(resimg)
        # 将 RGB 转换为 BGR
        result_cv = cv2.cvtColor(resimg, cv2.COLOR_RGB2BGR)

        # 显示结果帧
        cv2.imshow('Camera', result_cv)


        key=keyboard.get_key()
        if(key=='back'):
            break

        # 按 'q' 键退出
        if cv2.waitKey(1) == ord('q'):
            break

    # 释放摄像头资源
    cap.release()
    # 关闭所有 OpenCV 窗口
    cv2.destroyAllWindows()