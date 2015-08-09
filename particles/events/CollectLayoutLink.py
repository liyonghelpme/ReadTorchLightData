#coding:utf8
#收集粒子效果的 纹理贴图
#收集每个Layout的效果

#拷贝贴图到 Unity3d工程
#生成一个Json文件给Unity3d使用

import os
import sys
import codecs
import json
import re
stack = None
lines = None


readFile = sys.argv[1]

#读取堆栈名称
def readName(lineNo):
    lcon = lines[lineNo].encode('utf8')
    token = ''
    for c in lcon:
        if c == '[':
            pass
        elif c == ']':
            break
        else:
            token += c
    return token
#读取堆栈属性
def readProp(lcon):
    state = 0
    token = ''
    typ = ''
    key = ''
    value = ''
    for c in lcon:
        if state == 0:
            if c == '<':
                state = 1
        elif state == 1:
            if c == '>':
                state = 2
            else:
                typ += c
        elif state == 2:
            if c == ':':
                state = 3
            else:
                key += c
        elif state == 3:
            if c == '\n':
                pass
            elif c == '\r':
                pass
            else:
                value += c
    if typ == 'BOOL':
        try:
            value = bool(int(value))
        except:
            if value == 'true':
                value = True
            else:
                value = False
    elif typ == 'STRING':
        pass
    elif typ == 'FLOAT':
        value = float(value)
    else:
        pass
    

    return {key: value}, key, value

#lightFiles = set()

layoutLinks = []

layers = []

#进入一个stack进行递归读取
def readStack(lineNo):
    result = {
        'stackName' : readName(lineNo),
        'children' : [],
    }
    lineNo += 1

    #print 'readStack', result['stackName']
    #readStackName
    l = lineNo
    isLight = False
    isProp = False #读取的这个堆栈如果只是上个堆栈的一个属性则 stackName : Value 
    #读取DESCRIPTOR 如果是Particle 粒子 则设置Texture
    while  l < len(lines):
        lcon = lines[l].encode('utf8')
        if lcon[0] == '<':
            prop, key, value = readProp(lcon)
            print prop
            if key == 'VALUE':
                isProp = True
                
            if key == 'DESCRIPTOR' and value == 'Particle':
                isLight = True
                print 'isParticle'
                #layers.append(result)
                
            #print key
            if key == 'TEXTURE':
                #lightFiles.add(value)
                print 'readTexture', value
                layoutLinks.append(value)

            if result["stackName"] == "TEXTURE":
                print 'readTexture', value
                layoutLinks.append(value)

            result.update(prop)

        elif lcon[0] == '[':
            if lcon[1] == '/':
                if result["stackName"] == "BASEOBJECT" and isLight:
                #    layoutLinks.append()
                    layers.append(result)
                    isLight = False

                return result, l, isLight, isProp #堆栈当前结束位置

            else:
                con, l, isLight2, isProp = readStack(l)
                isLight = isLight or isLight2
            
                if result["stackName"] == "BASEOBJECT" and isLight:
                    print 'isLight'
                    layers.append(result)
                    isLight = False
                if isProp:
                    print con
                    result.update({con['stackName']: con['VALUE']})
                    isProp = False
                else:
                    result['children'].append(con)
        l += 1

    return result, l, isLight


def handleFunc(name):
    print "file", name
    global stack
    stack = []
    global lines
    lines = codecs.open(name, encoding='utf8').readlines()
    result, l, isLight, isProp = readStack(0)

    #生成Json文件
    output = '%s.json' % (name)
    print 'Generate JsonFile', output 
    resJson = json.dumps(result, separators=(', ', ': '), indent=4)
    wf = open(output, 'w')
    wf.write(resJson)
    wf.close()
    return resJson


def trans(cur, func):
    if not os.path.isdir(cur):
        return func(cur)
    else:
        allF = os.listdir(cur)
        for f in allF:
            name = os.path.join(cur, f)
            if os.path.isdir(name):
                trans(name, func)
                return
            elif name.find('.layout') != -1 and name.find('.json') == -1:
                fileContent = func(name)
                return

trans(readFile, handleFunc)


if not os.path.exists('fbx'):
    os.mkdir('fbx')

curDir = os.getcwd()

mediaPath = re.compile('media.*')

resDir = mediaPath.sub(curDir, '')
group = mediaPath.findall(curDir)
#print group

par = curDir.replace(group[0], '')
print par

#tarDir = os.path.join(curDir, 'fbx')
#tarDir = '/Users/liyong/u3dGame/xuexingDaLu/Assets'
tarDir = '/Users/liyong/Desktop/allUnity/Assets'
print 'imgNum', len(layoutLinks)
for png in layoutLinks:
    png = png.replace('\\', '/')
    fp = par+png
    srcDir = png.replace('.dds', '.png')
    realSrc = fp.replace('.dds', '.png')
    realTar = os.path.join(tarDir, srcDir.replace('media/', './'))
    print 'srcDir', srcDir
    print 'realTar', realTar 
    print 'copyFile###', realTar
    try:
        os.mkdirs(os.path.dirname(realTar))
    except:
        pass
    if not os.path.exists(realTar):
        print 'copyFile', realTar
        os.system('cp "%s" "%s" ' % (realSrc, realTar))
    else:
        print 'png exists', realTar

#print 'allPngs'
#print json.dumps(layoutLinks, separators=(', ', ': '), indent=4)

def format(s):
    return json.dumps(s, separators=(', ', ': '), indent=4)

lf = '%s_layers.json' % (readFile)
of = open(lf, 'w')
print 'save layers', lf 
mat = format(layers)
of.write(mat)
of.close()

#print mat
#print json.dumps(layoutLinks, separators=(', ', ': '), indent=4)

