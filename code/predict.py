from ultralytics import YOLO
from PIL import Image, ImageDraw
import os

MAXWIDTH=1000
MAXHEIGHT=1000

def init_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def split_image(image,tiles, rows, cols):
    # 读取图片
    # image = Image.open(image_path)
    width, height = image.size
    
    # 计算每个小块的宽度和高度
    tile_width = width // cols
    tile_height = height // rows
    
    # 存储所有分割后的图片
    for row in range(rows):
        for col in range(cols):
            left = col * tile_width
            upper = row * tile_height
            right = (col + 1) * tile_width
            lower = (row + 1) * tile_height
            
            # 使用Image.crop()进行图片切割
            tile = image.crop((left, upper, right, lower))
            tiles.append(tile)
    
    return tile_height,tile_width

def merge_tiles(tiles, rows, cols,tile_height, tile_width):
    # 创建空白的大图
    merged_image = Image.new('RGB', (cols * tile_width, rows * tile_height))
    
    for i, tile in enumerate(tiles):
        row = i // cols
        col = i % cols
        merged_image.paste(tile, (col * tile_width, row * tile_height))
    
    return merged_image

def pred_single(i,eachimg,model,resPath,show=False):
    result = model(eachimg)
    if show:
        result[0].show()  # display to screen
    result[0].save(resPath+f'/result{i}.jpg')

def pred_frame(i,eachimg,model,resPath,save=False):
    result = model(eachimg)
    if save:
        result[0].save(resPath+f'/frame{i}.jpg')
    return result[0]

def pred_split(i,eachimg,model,resPath,show=False):
    input_images=[]
    tile_height,tile_width=split_image(eachimg,input_images,3,3)
    results = model(input_images)  # return a list of Results objects
    # Process results list
    resList=[]
    resName=[]
    for j,result in enumerate(results):
        if show:
            result.show()  # display to screen
        init_dir(resPath)
        result.save(filename=resPath+f'/tmp_res{j}.jpg')  # save to disk
        resName.append(resPath+f'/tmp_res{j}.jpg')
        resList.append(Image.open(resPath+f'/tmp_res{j}.jpg'))
    merge_image=merge_tiles(resList,3,3,tile_height,tile_width)
    merge_image.save(resPath+f'/result{i}.jpg')
    for i in resName:
        os.remove(i)

def pred_pyramid(i,eachimg,model,resPath,show=False):
    
    merge_image=eachimg.copy()
    colorset=['red','green','blue']
    for k in range(3):
        col=k+1
        row=k+1
        input_images=[]
        merge_images=[]
        tile_height,tile_width=split_image(eachimg,input_images,row,col)
        tile_height,tile_width=split_image(merge_image,merge_images,row,col)
        results = model(input_images)
        for j,(result,image) in enumerate(zip(results,merge_images)):
            # if show:
            #     result.show()  # display to screen
            init_dir(resPath)
            if result.masks is not None:
                maskList=result.masks.xy
                boxList=result.boxes.xyxy.numpy()
                # 创建一个绘图对象
                draw = ImageDraw.Draw(image)
                # 绘制多边形
                for mask in maskList:
                    if len(mask)>0:
                        draw.polygon(mask, outline=colorset[k], fill=None, width=5)  # 可以设置outline和fill的颜色
                # for box in boxList:
                #     if len(box)>0:
                #         draw.rectangle(box, outline=colorset[k], fill=None, width=3)  # 可以设置outline和fill的颜色
                # image.show()
        merge_image=merge_tiles(merge_images,row,col,tile_height,tile_width)
    merge_image.save(resPath+f'/result{i}.jpg')
    if show:
        merge_image.show()

def get_single_result(i,image,resPath,model,show=False):
    width, height = image.size
    if width>MAXWIDTH or height>MAXHEIGHT:
    #     pred_split(i,image,model,resPath,show)
    # elif width>2*MAXWIDTH or height>2*MAXHEIGHT:
        pred_pyramid(i,image,model,resPath,show)
    else:
        pred_single(i,image,model,resPath,show)

def get_result(srcPath,resPath,model,show=False):
    init_dir(resPath)
    imageName=os.listdir(srcPath)
    src_images=[os.path.join(srcPath,each) for each in imageName]
    for i,eachimg in enumerate(src_images):
        image=Image.open(eachimg)
        get_single_result(i,image,resPath,model,show=show)



if __name__=='__main__':
    model = YOLO("runs/segment/419-all/weights/best.pt")  # load a custom model
    resPath='result/'
    srcPath='source/'
    # get_result(srcPath,resPath,model)
    src=Image.open('source/DSC_0339.JPG')
    # get_single_result(10,src,resPath,model,show=1)
    pred_single(10,src,model,resPath,show=1)
    # src.show()
