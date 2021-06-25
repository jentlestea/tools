import os
import random
import fcntl

LOCKPATH = "../dataBase/.lockf"
flockfd = None

def flock():
	global flockfd
	fcntl.flock(flockfd, fcntl.LOCK_EX)
def funlock():
	global flockfd
	fcntl.flock(flockfd, fcntl.LOCK_UN)

def prepare():
	global flockfd
	if flockfd == None:
		flockfd = open(LOCKPATH)
def clean():
	global flockfd
	if flockfd != None:
		flockfd.close()
	flockfd = None

def select(user, commitID):
	ret = ['-1', None]
	commitIDs=[]
	contents=[]
	with open("../dataBase/frozen.usr") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 3:
				return ret
			if content[0] == commitID and content[2] == user:
				ret = [content[0], content[1]]
				return ret
			if content[0] == commitID and content[2] != user:
				return ret
	with open("../dataBase/candidates") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 2:
				return ret
			contents.append(content)
	if len(contents) == 0:
		return ret

	if commitID == '0':
		rd = random.randint(0, len(contents))
		ret = contents[rd]
	else:
		for c in contents:
			if commitID == c[0]:
				ret = c
	if ret[0] != '-1':
		wc = [ret[0], ret[1], user]

	with open("../dataBase/frozen.usr", 'a') as f:
		f.write("{0[0]} {0[1]} {0[2]}\n".format(wc))
	return ret

def lockSelect(user, commitID):
	flock()
	ret = select(user, commitID)
	funlock()
	return ret

def cancel(user, commitID):
	contents=[]
	found = 0
	with open("../dataBase/frozen.usr") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 3:
				return -1
			if content[0] == commitID:
				found = 1
				continue
			contents.append(content)
	with open("../dataBase/frozen.usr", 'r+') as f:
		f.truncate()
		for line in contents:
			f.write("{0[0]} {0[1]} {0[2]}\n".format(line))
	return found

def lockCancel(user, commitID):
	flock()
	ret = cancel(user, commitID)
	funlock()
	return ret

def show(user):
	ret = []
	with open("../dataBase/candidates") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 2:
				return -1
			ftype = os.popen('bash get_type.sh {0[0]}'.format(content))
			type = ftype.read()
			fscore = os.popen('bash get_score.sh {0[0]}'.format(content))
			score = fscore.read()
			showinfo = [content[0], content[1], '0', type, score]
			ret.append(showinfo)
	with open("../dataBase/frozen.usr") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 3:
				return -1
			for i in ret:
				if i[0] == content[0] and user != content[2]:
					ret.remove(i)
				if i[0] == content[0] and user == content[2]:
					i[2] = '1'
	return ret

def lockShow(user):
	flock()
	ret = show(user)
	funlock()
	return ret
