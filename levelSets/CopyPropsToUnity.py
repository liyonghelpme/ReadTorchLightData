#coding:utf8
'''
拷贝props 文件夹下面的fbx 文件 到unity 工程的 levelsets/props目录里面
'''
import os
import sys
import json

if not os.path.exists('copyProps'):
    os.mkdir('copyProps')

copyCount = 0
copyFbx = 0
def copyCur(cur):
    print 'copy', cur
    f = os.listdir(cur)
    for i in f:
        name = os.path.join(cur, i)
        if os.path.isdir(name):
            pass
        else:
            #os.makedirs(os.path.join('copyProps', ))
            os.system('cp %s %s' % (name, os.path.join('copyProps', i)))
            global copyCount
            if i.find('.fbx') != -1:
                global copyFbx
                copyFbx += 1
            copyCount += 1

def trans(cur):
    if cur.find('fbx') != -1:
        copyCur(cur)
    else:
        f = os.listdir(cur)
        for i in f:
            name = os.path.join(cur, i)
            if os.path.isdir(name):
                trans(name)
            else:
                pass

trans('props')

print 'Copy Count', copyCount
print 'fbx', copyFbx
