#coding:utf8
#读取第一个 .layout文件
#输出所有的 Props 场景小挂件 layoutLinks
#用于分析每个场景组件是如何制作的读取配置 在unity自动组装

import os
import sys
import codecs
import json
stack = None
lines = None

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
    while  l < len(lines):
        lcon = lines[l].encode('utf8')
        if lcon[0] == '<':
            prop, key, value = readProp(lcon)
            if key == 'DESCRIPTOR' and value == 'Layout Link':
                isLight = True
            elif isLight and key == 'LAYOUT FILE':
                #lightFiles.add(value)
                layoutLinks.append(value)

            result.update(prop)

        elif lcon[0] == '[':
            if lcon[1] == '/':
                return result, l #堆栈当前结束位置
            else:
                con, l = readStack(l)
                result['children'].append(con)
        l += 1

    return result, l


def handleFunc(name):
    print "file", name
    global stack
    stack = []
    global lines
    lines = codecs.open(name, encoding='utf16').readlines()
    result, l = readStack(0)

    #print json.dumps(result, separators=(', ', ': '), indent=4)


def trans(cur, func):
    allF = os.listdir(cur)
    for f in allF:
        name = os.path.join(cur, f)
        if os.path.isdir(name):
            trans(name, func)
            return
        elif name.find('.layout') != -1 and name.find('.json') == -1:
            fileContent = func(name)
            return

trans('.', handleFunc)

print json.dumps(layoutLinks, separators=(', ', ': '), indent=4)


