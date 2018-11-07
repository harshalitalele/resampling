#Convert image and save

from PIL import Image

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

def testImageArrays():
    testImg = Image.open("E:/Studies/POCs/resampling/test01.png", 'r')
    width, height = testImg.size
    testArr = testImg.convert('RGBA')

    newImg = Image.new('RGB', (5, 5), color = (255,255,255))
    newImgArr = newImg.load()
    for i in range(0, 5):
        for j in range(0, 5):
            xy = (i, j)
            print("x,y: ", xy)
            rgb = testArr.getpixel(xy)
            newImgArr[i, j] = (rgb[0], rgb[1], rgb[2])
    newImgPath = "E:/Studies/POCs/resampling/newTestImg.jpg"
    newImg.save(newImgPath)

def downsampleImage(imagePath):
    origImage = Image.open(imagePath, 'r')
    width, height = origImage.size
    downimg = Image.new('RGB', (round((width+0.8)/2), round((height+0.8)/2)), color = (0,0,0))
    rgbimage = origImage.convert('RGBA')
    newdownimage = downimg.load()
    for i in range(0, width):
        for j in range(0, height):
            xy = (i, j)
            rgb = rgbimage.getpixel(xy)
            if(i%2==0 and j%2==0):
                newdownimage[round((i+0.8)/2), round((j+0.8)/2)] = (rgb[0], rgb[1], rgb[2])            
    newDownImagePath = "E:/Studies/POCs/resampling/testDown.jpg"
    downimg.save(newDownImagePath)

def getUpimgsize(wd, ht):
    upWd = 0
    upHt = 0
    downsize = round((wd+0.8)/2)*round((ht+0.8)/2)
    upsize = wd*ht - downsize
    upWd = upHt = upsize**(1/2)
    while(upWd != 0 and upHt != 0 and not(upWd == int(upWd) and upHt == int(upHt))):
        upWd = int(upWd - 1)
        upHt = upsize/upWd
    return (int(upWd), int(upHt))

def upsampleImage(imagePath):
    origImage = Image.open(imagePath, 'r')
    width, height = origImage.size
    upWd, upHt = getUpimgsize(width, height)
    print("actual size ", (width, height))
    print("upsize: ", (upWd, upHt))
    upimg = Image.new('RGB', (upWd, upHt), color = (0,0,0))
    rgbimage = origImage.convert('RGBA')
    newupimage = upimg.load()
    uindex = 0
    for j in range(0, height):
        for i in range(0, width):
            xy = (i, j)
            rgb = rgbimage.getpixel(xy)
            if(not(i%2==0 and j%2==0)):
                #print("uindex : ", (uindex % upWd, uindex // upWd))
                newupimage[uindex % upWd, uindex // upWd] = (rgb[0], rgb[1], rgb[2])
                uindex = uindex + 1
    newUpImagePath = "E:/Studies/POCs/resampling/testUp.jpg"
    upimg.save(newUpImagePath)

def resampleImage(imagePath, newDownImageName, newUpImageName):
    origImage = Image.open(imagePath, 'r')
    width, height = origImage.size
    downImgWd = round((width+0.8)/2)
    downImgHt = round((height+0.8)/2)
    downimg = Image.new('RGB', (downImgWd, downImgHt), color = (0,0,0))
    upWd, upHt = getUpimgsize(width, height)
    upimg = Image.new('RGB', (upWd, upHt), color = (0,0,0))
    rgbimage = origImage.convert('RGBA')
    newdownimage = downimg.load()
    newupimage = upimg.load()
    upIndex = 0
    for j in range(0, height):
        for i in range(0, width):
            xy = (i, j)
            rgb = rgbimage.getpixel(xy)
            if(not(i%2==0 and j%2==0)):
                newupimage[upIndex % upWd, upIndex // upWd] = (rgb[0], rgb[1], rgb[2])
                upIndex = upIndex + 1
                continue
            newdownimage[round(i/2 + 0.4), round(j/2 + 0.4)] = (rgb[0], rgb[1], rgb[2])
    newDownImagePath = "E:/Studies/POCs/resampling/" + newDownImageName + ".jpg"
    newUpImageName = "E:/Studies/POCs/resampling/" + newUpImageName + ".jpg"
    downimg.save(newDownImagePath)
    upimg.save(newUpImageName)

def superImpose():
    downImage = Image.open("E:/Studies/POCs/resampling/downFlow.jpg", 'r')
    dwd, dht = downImage.size
    dimgArr = downImage.convert('RGB')
    upImage = Image.open("E:/Studies/POCs/resampling/upFlow.jpg", 'r')
    uimgArr = upImage.convert('RGB')
    uwd, uht = upImage.size
    newimg = Image.new('RGB', (dwd*2, dht*2), color = (0,0,0))
    nwd, nht = newimg.size
    newimgArr = newimg.load()
    upointer = 0
    dpointer = 0
    for i in range(0, dwd*2):
        for j in range(0, dht*2):
            if(i%2==0 or j%2==0):
                xy = (upointer%uwd, upointer//uwd)
                upx = uimgArr.getpixel(xy)
                newimgArr[i, j] = (upx[0],upx[1],upx[2])
                upointer = upointer + 1
                continue
            xy = (i//2, j//2)
            dpx = dimgArr.getpixel(xy)
            newimgArr[i, j] = (dpx[0],dpx[1],dpx[2])
    newImagePath = "E:/Studies/POCs/resampling/superImposed.jpg"
    newimg.save(newImagePath)
    
#createSampleImg()
resampleImage("E:/Studies/POCs/resampling/test.png", "downFlow", "upFlow")
#superImpose()
#downsampleImage("E:/Studies/POCs/resampling/test.png")

#testImageArrays()
#upsampleImage("E:/Studies/POCs/resampling/test.png")

