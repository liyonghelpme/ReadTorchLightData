import PIL
from PIL import Image
import xml
import xml.sax
import xml.sax.handler
import os

'''
切割cegui xml 的图集文件为单张图片itemicons 文件 
'''

#filename = "itemicons5.imageset"
#expName = "export13"

class ImageHandler(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.imgs = []
	def startDocument(self):
		pass

	def startElement(self, name, attrs):
		if name == "Image":
			imgData = {}
			imgData["name"] = str(attrs.get("Name", ""))
			imgData["pos"] = (int(attrs.get("XPos")),
				 int(attrs.get("YPos")), 
				 int(attrs.get("Width")), 
				 int(attrs.get("Height")), 
				 int(attrs.get("XOffset", 0)), 
				 int(attrs.get("YOffset", 0)) ) 
			self.imgs.append(imgData)

		if name == "Imageset":
			fi = str(attrs.get("Imagefile"))
			self.imgFile = fi.replace("media/ui/", '').replace("dds", "png")


	def endElement(self, name):
		pass



allIcon = os.listdir('itemicons')
for i in allIcon:
    name = os.path.join('itemicons', i)
    if name.find('.imageset') != -1:
        parser = xml.sax.make_parser()
        handler = ImageHandler()
        parser.setContentHandler(handler)
        parser.parse(open(name))
        print handler.imgs

        imf = Image.open(handler.imgFile)
        print imf

        expName = i.replace('.imageset', '')+'Dir'
        if not os.path.exists(expName):
            os.mkdir(expName)

        for im in handler.imgs:
            p = im["pos"]
            nim = imf.crop(box=(p[0], p[1], p[0]+p[2], p[1]+p[3]))
            #print("savename "+i[])
            nim.save(expName+"/"+im["name"]+".png")

