#coding:utf8
import os
import re
import sys
di = sys.argv[1]



def tran(cur):
    f = os.listdir(cur)
    for i in f:
        name = os.path.join(cur, i)
        if name.find('.dds') != -1:
            os.system('nconvert -out png %s' % (name))
        elif os.path.isdir(name):
            tran(name)

print 'convert directory '+di
tran(di)

