#coding:utf8
#解析树状结构文本
import os
import re
import codecs
#start
pat = re.compile("\[([\w\s]+)\]")
#end
pat2 = re.compile("\[/([\w\s]+)\]")
#id
pat3 = re.compile("<INTEGER>ID:(\d+)")
#child list
pat4 = re.compile("<INTEGER>child(\d*):(\d+)")
stack = []

root = -1
tree = {}

f = codecs.open("unittypes.hie", encoding='utf16').readlines()
maxStack = 0
curID = -1
for l in f:
	res = pat.findall(l)
	if len(res) > 0:
		stack.append(res)
	res2 = pat2.findall(l)
	if len(res2) > 0:
		stack.pop(-1)
	ID = pat3.findall(l)
	if len(ID) > 0:
		curID = int(ID[0])
		tree[curID] = {'name':stack[-1], 'child':[]}

	child = pat4.findall(l)
	if len(child) > 0:
		tree[curID]['child'].append(int(child[0][1]))

	if len(stack) > maxStack:
		maxStack = len(stack)
	#print stack


print 'max is ', maxStack

#print tree

for t in tree:
	print 'define', t, 'define', tree[t]['name'][0]
	#print tree[t]['child']
	for c in tree[t]['child']:
		print c, tree[c]["name"][0], 
	print 	
	print 