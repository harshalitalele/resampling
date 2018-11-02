#Convert image and save

from PIL import Image

def resampleImage(imagePath, newDownImageName, newUpImageName):
    origImage = Image.open(imagePath, 'r')
    width, height = origImage.size
    print("img width ", width)
    print("img height ", height)
    downimg = Image.new('RGB', (width//2, height//2), color = (0,0,0))
    upsize = int(((3*width*height)**(1/2))/2)+1
    print("upimg width ", upsize)
    upimg = Image.new('RGB', (upsize, upsize), color = (0,0,0))
    rgbimage = origImage.convert('RGBA')
    newdownimage = downimg.load()
    newupimage = upimg.load()
    upIndex = 0
    upmaxWd = upsize
    for i in range(0, width):
        for j in range(0, height):
            xy = (i, j)
            rgb = rgbimage.getpixel(xy)
            if(i%2==0 or j%2==0):
                newupimage[upIndex // upmaxWd, upIndex % upmaxWd] = (rgb[0], rgb[1], rgb[2])
                upIndex = upIndex + 1
                continue            
            newdownimage[i//2, j//2] = (rgb[0], rgb[1], rgb[2])
    newDownImagePath = "E:/Studies/POCs/resampling/" + newDownImageName + ".jpg"
    newUpImageName = "E:/Studies/POCs/resampling/" + newUpImageName + ".jpg"
    downimg.save(newDownImagePath)
    upimg.save(newUpImageName)

def createSampleImg():
    newimg = Image.new('RGBA', (500,500), color = (0,0,0,255))
    newimgArr = newimg.load()
    for i in range(0, 500):
        for j in range(0, 500):
            if(i%2==0 or j%2==0):
                newimgArr[i,j] = (0,255,0,255)
                continue
            newimgArr[i,j] = (255,0,0,255)
    newImagePath = "E:/Studies/POCs/resampling/createdImg.png"
    newimg.save(newImagePath)

#createSampleImg()
resampleImage("E:/Studies/POCs/resampling/flowers.png", "downFlow", "upFlow")
