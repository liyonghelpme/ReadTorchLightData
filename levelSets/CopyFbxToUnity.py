#coding:utf8
'''
将map.json 中所有的fbx 资源拷贝到合适的位置
/Users/liyong/u3dGame/xuexingDaLu/Assets/levelsets 目录
'''
import json
import os
import re

levelSets = re.compile('levelsets/.*')

u3dHome = '/Users/liyong/u3dGame/xuexingDaLu/Assets' 

fc = json.loads(open('map.json').read())

def correctPath(oldPath):
    dirs = oldPath.split('/')
    newPath = '/'
    
    for d in dirs:
        if d != '':
            lists = os.listdir(newPath)
            find = False
            for l in lists:
                if l.lower() == d.lower():
                    newPath = os.path.join(newPath, l)
                    find = True
                    break
            if not find:
                return None
    return newPath
        
            

def CopyFile(fn, countNum):
    fn = os.path.join('/Users/liyong/Desktop/', fn)
    #print fn
    oldDir = os.path.dirname(fn)
    dirn = os.path.join(os.path.dirname(fn), 'fbx')
    fname = os.path.basename(fn).replace('.mesh', '.fbx')
    fbx = os.path.join(dirn, fname)
    
    u3dFName = os.path.join(oldDir, fname)
    #print fbx
    lv = levelSets.findall(u3dFName)
    if len(lv) > 0:
        #print lv[0]
        u3dFbx = os.path.join(u3dHome, lv[0])
        #fn = correctPath(fn)
        if fn == None:
            return
        print 'correct', fn
        #FIXME:包含有动画的fbx 文件需要拷贝动画等元素
        if not os.path.exists(fbx):
            return
        oldLen = len(open(fbx, 'r').read())
        exist =  os.path.exists(u3dFbx)
        if exist:  
            newLen = len(open(u3dFbx, 'r').read())
        else:
            newLen = 0

        #os.listdir()
        print 'len', oldLen, newLen
        if newLen  < oldLen:
            print 'no', u3dFbx
            print 'oldFile', fbx
            #print 'old', os.path.exists(fn)
            try:
                os.makedirs(os.path.dirname(u3dFbx))
            except Exception as e:
                print e
                pass
            #找到正确的本地文件
            os.system('cp "%s" "%s"' % (fbx, u3dFbx))
            if countNum:
                global fail
                fail += 1
        else:
            print 'has', u3dFbx


fail = 0
for k in fc:
    v = fc[k]
    fn  = v['FILE']
    col = v.get('COLLISIONFILE')
    CopyFile(fn, True)
    if col != None:
        CopyFile(col, False)

    #os.path.join(u3dHome)


print 'total fail', len(fc), fail

 


