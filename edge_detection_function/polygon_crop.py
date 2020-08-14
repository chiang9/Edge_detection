import tkinter as Tkinter
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import sys

def img_crop(path, basewidth = 500):
    pp = polygon_select(path, basewidth)
    newIm = polygon_crop(path, pp)
    return newIm

def polygon_select(path, basewidth = 500):
    window = Tkinter.Tk(className="bla")
    clickList = list()

    image = Image.open(path)
    wid_ratio = basewidth/image.size[0]
    baselength = int(round(image.size[1] * wid_ratio))
    image = image.resize((basewidth, baselength), Image.ANTIALIAS)

    canvas = Tkinter.Canvas(window, width=image.size[0], height=image.size[1])
    canvas.pack()
    image_tk = ImageTk.PhotoImage(image)

    canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)

    def callback(event):
        print ("clicked at: "+ str(event.x), str(event.y))
        clickList.append((int(round(event.x/wid_ratio)), int(round(event.y/wid_ratio))))

    canvas.bind("<Button-1>", callback)
    Tkinter.mainloop()
    return clickList


def polygon_crop(path, polygon):
    im = Image.open(path).convert("RGBA")
    imArray = np.asarray(im)

    maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
    ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
    mask = np.array(maskIm)

    newImArray = np.empty(imArray.shape,dtype='uint8')
    newImArray[:,:,:3] = imArray[:,:,:3]
    newImArray[:,:,3] = mask*255

    newIm = Image.fromarray(newImArray, "RGBA")
    return newIm