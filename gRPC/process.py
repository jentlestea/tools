import os
import random
import fcntl
import time

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

def record(user, line):
	path = "../database/person/{0}".format(user)
	with open(path, 'a+') as f:
		f.write("["+time.asctime(time.localtime(time.time()))+"] "+"{0}\n".format(line))

def getRecord(user):
	path = "../dataBase/person/{0}".format(user)
	if os.path.exists(path) == False:
		return -1, ""
	lines = None
	with open(path) as f:
		lines = f.readlines()
	record = ""
	for line in lines:
		record = record + line
	return 0, record

def select(user, commitID):
	ret = ['-1', None]
	commitIDs=[]
	contents=[]
	with open("../dataBase/frozen.usr") as f:
		lines = f.readlines()
		times = 0
		ltsTimes = 0
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 3:
				return ret
			if content[0] == commitID and content[2] == user:
				ret = [content[0], content[1]]
				return ret
			if content[0] == commitID and content[2] != user:
				return ret
			if content[2] == user:
				times += 1
				ftype = os.popen('bash get_type.sh {0}'.format(content[0]))
				type = ftype.read().strip('\n')
				if type.find("LTS") != -1:
					ltsTimes += 1
		if times >= 5 or ltsTimes >= 3:
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
		record(user, "Select commitID:{0}".format(ret[0]))
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
	if found == 1:
		record(user, "Cancel commitID:{0}".format(commitID))
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
			ftype = os.popen('bash get_type.sh {0}'.format(content[0]))
			type = ftype.read().strip('\n')
			fscore = os.popen('bash get_score.sh {0}'.format(type))
			score = fscore.read().strip('\n')
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
	record(user, "Show commitIDs")
	return ret

def lockShow(user):
	flock()
	ret = show(user)
	funlock()
	return ret

def history(user):
	return getRecord(user)

def lockHistory(user):
	flock()
	ret, __history = history(user)
	funlock()
	return ret, __history
