#coding:utf8
#读取Graph 中的数据 并且绘制成一个曲线
import os
import sys
import codecs
import json
import matplotlib.pyplot as plt
import numpy

#f = sys.argv[1]

'''
{
    stackName:line,
    key:value,
    key:value,
    children:[
        {
            stackName:point,

        },
        {

        }
    ]
}
'''
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
        value = bool(int(value))
    elif typ == 'STRING':
        pass
    elif typ == 'FLOAT':
        value = float(value)
    else:
        pass

    return {key: value}

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
    while  l < len(lines):
        lcon = lines[l].encode('utf8')
        if lcon[0] == '<':
            result.update(readProp(lcon))
        elif lcon[0] == '[':
            if lcon[1] == '/':
                return result, l #堆栈当前结束位置
            else:
                con, l = readStack(l)
                result['children'].append(con)
        l += 1

    return result, l




def draw(key, value):
    #plt.plot(key, value)
    #plt.show()
    coefficients = numpy.polyfit(key, value, 3)
    polynomial = numpy.poly1d(coefficients)
    ys = polynomial(key)
    print coefficients
    print polynomial

    plt.plot(key, value, 'o')
    plt.plot(key, ys)
    #plt.show()

#k v

def getKeyValue(result):
    collectData = []
    colVal = []
    for p in result['children']:
        collectData.append(p["X"])
        colVal.append(p["Y"])
    return collectData, colVal
    #draw(collectData, colVal)

def drawFile(f):
    print "drawFile", f
    global stack
    stack = []
    global lines
    lines = codecs.open(f, encoding='utf16').readlines()

    result, l = readStack(0)
    print type(result)
    #print result

    print json.dumps(result, separators=(', ', ': '), indent=4)
    collectData, colVal = getKeyValue(result)
    draw(collectData, colVal)

def readFile(f):
    print 'readFile', f
    global stack
    stack = []
    global lines
    lines = codecs.open(f, encoding='utf16').readlines()

    result, l = readStack(0)
    print type(result)
    return result

def divData(f1, f2):
    k1, v1 = getKeyValue(f1)
    k2, v2 = getKeyValue(f2)
    tk = [0]*len(k1)
    tv = [0]*len(k1)
    for i in xrange(0, len(k1)):
        tk[i] = k1[i]
        tv[i] = v1[i]/v2[min(len(v2)-1, i)] 
    draw(tk, tv)

#读取多个文件参数
#绘制每个 文件
#最后显示
#需要多少只怪物
def main():
    if sys.argv[1] == 'div':
        f1 = readFile(sys.argv[2])
        f2 = readFile(sys.argv[3])
        divData(f1, f2)
        plt.show()
    else:
        for i in xrange(1, len(sys.argv)):
            drawFile(sys.argv[i])
        plt.show()

main()
         
            
            
           


