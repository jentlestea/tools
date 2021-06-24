import os
import random
import fcntl

LOCKPATH = "../dataBase/.lockf"
flockfd = None

def flock():
	flockfd = open(LOCKPATH)
	fcntl.flock(flockfd, fcntl.LOCK_EX)
def funlock():
	fcntl.flock(flockfd.fcntl.LOCK_UN)
	close(flockfd)

def select(user, commitID):
	ret = [None, None]
	commitIDs=[]
	contents=[]
	with open("../dataBase/frozen.usr") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 3:
				return -1
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
				return -1
			contents.append(content)
	if len(contents) == 0:
		return -1

	if commitID == '0':
		rd = random.randint(0, len(contents))
		ret = contents[rd]
	else:
		for c in contents:
			if commitID == c[0]:
				ret = c

	if ret[0] != None:
		wc = [ret[0], ret[1], user]

	with open("../dataBase/frozen.usr", 'a') as f:
		f.write("{0[0]} {0[1]} {0[2]}".format(wc))
	return ret

def lockSelect(user, commitID):
	flock()
	ret = select(user, commitID)
	funlock()
	return ret

def cancel(user, commitID):
	contents=[]
	with open("../dataBase/frozen.usr") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 3:
				return -1
			if content[0] == commitID:
				continue
			contents.append(content)
	with open("../dataBase/frozen.usr", 'a') as f:
		f.truncate()
	for line in contents:
		f.write("{0[0]} {0[1]} {0[2]}".format(line))

def lockCancel(user, commitID):
	flock()
	cancel(user, commitID)
	funlock()

def show(user):
	ret = []
	with open("../dataBase/candidates") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 2:
				return -1
			showinfo = [content[0], content[1], '0']
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

def lockSelect(user, commitID):
	flock()
	ret = select(user, commitID)
	funlock()
	return ret
