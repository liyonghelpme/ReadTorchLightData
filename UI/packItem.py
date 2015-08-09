import PIL
from PIL import Image
import xml
import xml.sax
import xml.sax.handler
import os

'''
合并ItemToolTip 的若干张离散图片为一张 完整九宫格图片
'''
imname = ["TopLeft", "TopEdge", "TopRight", 
	"LeftEdge", "Middle", "RightEdge",
	"BottomLeft", "BottomEdge", "BottomRight",
]

ims = []
size = None
for i in xrange(0, 9):
	im = Image.open("ItemTooltip"+imname[i]+".png")
	ims.append(im)
	size = im.size


totalSize = [size[0]*3, size[1]*3]
c = 0
im = Image.new("RGBA", totalSize)
for i in ims:
	im.paste(i, ((c%3)*size[0], (c/3)*size[1]))
	c = c+1

im.save("ItemTooltip.png")
