#coding:utf8
'''
生成mine.dat 所有的地图组成块 组件信息转化为 json 文件， 用于unity中加载使用 
将组成mine的 所有地表组件 的 name 和 对应的guid 对应起来
'''
import json
import re
import codecs
import os
import json
import sys

piece = re.compile("\[PIECE\]")
endpiece = re.compile("\[/PIECE\]")
fileName = re.compile(">FILE:([\w/\.\d]+)")
colFile = re.compile(">COLLISIONFILE:([\w/\.\d]+)")
guid = re.compile("GUID:(\-?\d+)")
name = re.compile("NAME:([\w_\d]+)")

fi = sys.argv[1]

'''
guid: {filename, collisionfile, name}
'''
exportJson = {
}

inPiece = False
fn = None
cn = None
gid = None
n = None

lines = codecs.open(fi, encoding='utf16', mode='rb').readlines()
count = 0
endPieceNum = 0
readPiece = 0
for l in lines:
    l = l.encode('utf8')

    ret = piece.findall(l)
    if len(ret) > 0:
        inPiece = True
        count += 1
        #print ret, len(ret)
    ret = endpiece.findall(l)
    if len(ret) > 0:
        inPiece = False
        
        exportJson[gid] = {
            'filename' : fn,
            'collisionfile' : cn,
            'name' : n,
            'guid' : gid,
        }
        fn = None
        cn = None
        n = None
        gid = None
        endPieceNum += 1
        
    if inPiece:
        #readPiece += 1
        ret = guid.findall(l)
        if len(ret) > 0:
            gid = ret[0]

        ret = fileName.findall(l)
        if len(ret) > 0:
            fn = ret[0]

        ret = colFile.findall(l)
        if len(ret) > 0:
            cn = ret[0]

        ret = name.findall(l)
        if len(ret) > 0:
            n = ret[0]
            #print n


print 'readPiece', count
print 'piecesNum', len(exportJson)
print 'endPiece', endPieceNum
print 'read', readPiece
nf = open(fi+'.json', 'w')
nf.write(json.dumps(exportJson, separators=(', ', ': '), indent=4))
nf.close()
