#coding:utf8

'''
用于将火炬之光 关卡布局 layout中 特定Layout文件导出为json文件， 用于unity中加载使用

unity读取json 来加载关卡布局
'''
import os
import sys
import json
import re
import codecs

di = sys.argv[1]
print di
#objects Room Pieces
#children
'''
children
baseobject 
properties
DESCRIPTION ROOM Pieces
POSITION x y z
forward rotate 
right 
up 0 1 0
guid---> 

/properties

/baseobject
/children
'''

#读取properties
#读取属性 描述
#读取 position 和 forward right 属性
#读取 guid 属性
prop = re.compile("\[PROPERTIES\]")
endProp = re.compile("\[/PROPERTIES\]")
desc = re.compile("DESCRIPTOR:Room Piece")
posx = re.compile("POSITIONX:((\-)?\d+(\.\d+)?(e-?\d+)?)")
posy = re.compile("POSITIONY:((\-)?\d+(\.\d+)?(e-?\d+)?)")
posz = re.compile("POSITIONZ:((\-)?\d+(\.\d+)?(e-?\d+)?)")

forx = re.compile("FORWARDX:((\-)?\d+(\.\d+)?(e-?\d+)?)")
fory = re.compile("FORWARDY:(\-?\d+(\.\d+)?(e-?\d+)?)")
forz = re.compile("FORWARDZ:(\-?\d+(\.\d+)?(e-?\d+)?)")

rix = re.compile("RIGHTX:(\-?\d+(\.\d+)?(e-?\d+)?)")
riy = re.compile("RIGHTY:(\-?\d+(\.\d+)?(e-?\d+)?)")
riz = re.compile("RIGHTZ:(\-?\d+(\.\d+)?(e-?\d+)?)")



guid = re.compile('GUID:(\-?\d+)')

readPropsCount = 0
endPropsCount = 0
def readPieces(lines):
	exportJson = []

	inProp = False
	px = 0
	py = 0
	pz = 0
	fx = 0
	fy = 0
	fz = 1
	rx = 1
	ry = 0
	rz = 0
	gid = 0

	isRoomPieces = False
	for l in lines:
		#convert to string
		l = l.encode('utf8')

		ret = prop.findall(l)
		if len(ret) > 0:
			inProp = True
			global readPropsCount

			readPropsCount += 1
			gid = 0
			px = 0
			py = 0
			pz = 0

			fx = 0
			fy = 0
			fz = 1

			rx = 1
			ry = 0
			rz = 0

		ret = endProp.findall(l)
		if len(ret) > 0:
			inProp = False
			if isRoomPieces:
				isRoomPieces = False
				exportJson.append({
					"guid":gid,
					"posx":px,
					"posy":py,
					"posz":pz,

					"forx":fx,
					"fory":fy,
					"forz":fz,

					"rix":rx,
					"riy":ry,
					"riz":rz,
					})
			#print "clear Props"	
			global endPropsCount
			endPropsCount += 1
			

		if inProp:
			ret = desc.findall(l)
			if len(ret) > 0:
				isRoomPieces = True
			ret = posx.findall(l)
			if len(ret) > 0:
				px = float(ret[0][0])

			ret = posy.findall(l)
			if len(ret) > 0:
				py = float(ret[0][0])

			ret = posz.findall(l)
			if len(ret) > 0:
				pz = float(ret[0][0])

			ret = forx.findall(l)
			if len(ret) > 0:
				fx = float(ret[0][0])
			
			ret = fory.findall(l)
			if len(ret) > 0:
				fy = float(ret[0][0])

			ret = forz.findall(l)
			if len(ret) > 0:
				fz = float(ret[0][0])
			
			ret = rix.findall(l)
			if len(ret) > 0:
				rx = float(ret[0][0])
			
			ret = riy.findall(l)
			if len(ret) > 0:
				ry = float(ret[0][0])
			
			ret = riz.findall(l)
			if len(ret) > 0:
				rz = float(ret[0][0])
			
			ret = guid.findall(l)
			if len(ret) > 0:
				gid = ret[0]
	return exportJson		

allLayout = []

def handleLayout(name):
    print 'readFile', name
    i = os.path.basename(name)

    lines = codecs.open(name, encoding='utf16', mode='rb').readlines()
    ret = readPieces(lines)
    ret = {
        'pieces' : ret,
        "name": i,
    }
    allLayout.append(ret)
    #return ret
    return allLayout
        

def trans(cur):
    if os.path.isdir(cur):
        f = os.listdir(cur)
        for i in f:
            name = os.path.join(cur, i)
            if os.path.isdir(name):
                trans(name)
            else:
                if name.find('.layout') != -1:
                    return handleLayout(name)
    else:
        return handleLayout(cur)
        


ret = trans(di)
sf = di+'.json'
nf = open(sf, 'w')

nf.write(json.dumps(ret, separators=(', ', ': '), indent=4, sort_keys=True))
nf.close()

print readPropsCount
print endPropsCount
print 'saveFile', sf
