import os
import random
import fcntl
import time
import _thread

LOCKPATH = "../dataBase/.lockf"
flockfd = None
#workOnHome = os.getenv('WORKON_HOME')

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
	try:
		_thread.start_new_thread(lockClearFrozen, ())
	except:
		print('ERROR: create clear frozen thread failed')

def clean():
	global flockfd
	if flockfd != None:
		flockfd.close()
	flockfd = None

lockTimeMap = {}
def setFrozen(commitID):
	global lockTimeMap
	time = time.time()
	lockTimeMap[commitID] = time

#2 day frozen
frozenTime = 60*60*24*2
def lockClearFrozen():
	flock()
	currentTime = time.time()
	lines = None
	with open("../dataBase/frozen.usr") as f:
		lines = f.readlines()
	with open("../dataBase/frozen.usr", 'w+') as f:
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 3:
				return ret
			if lockTimeMap.has_key(content[0]) == False:
				print("ERROR: {0} not found when clear frozen".format(content[0]))
				continue
			div = currentTime - lockTimeMap[content[0]]
			if div < frozenTime:
				f.write("{0[0]} {0[1]} {0[2]}\n".format(content))
			else:
				del lockTimeMap[content[0]]
	funlock()

def record(user, line):
	path = "../dataBase/person/{0}".format(user)
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
	lockLTS = False
	with open("../dataBase/person/LTSList") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n")
			if content.find(user) != -1:
				lockLTS = True
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
		if times >= 2 or ltsTimes >= 1:
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
		type = 'LTS'
		while type.find('LTS') != -1:
			rd = random.randint(0, len(contents))
			ret = contents[rd]
			ftype = os.popen('bash get_type.sh {0}'.format(ret[0]))
			type = ftype.read().strip('\n')
	else:
		for c in contents:
			if commitID == c[0]:
				ret = c
				ftype = os.popen('bash get_type.sh {0}'.format(commitID))
				type = ftype.read().strip('\n')
				if type.find('LTS') != -1 and lockLTS == True:
					ret[0] = '-1'
	if ret[0] != '-1':
		wc = [ret[0], ret[1], user]
		with open("../dataBase/frozen.usr", 'a') as f:
			f.write("{0[0]} {0[1]} {0[2]}\n".format(wc))
		setFrozen(ret[0])
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

def show(user, commitID, selected):
	ret = []
	if commitID != '0' or selected != '0':
		if selected == 'selected':
			with open("../dataBase/frozen.usr") as f:
				lines = f.readlines()
				for line in lines:
					content = line.strip("\n").split()
					if len(content) != 3:
						print("OQServer ERROR: frozen.usr format error")
						continue
					ftype = os.popen('bash get_type.sh {0}'.format(content[0]))
					type = ftype.read().strip('\n')
					fscore = os.popen('bash get_score.sh {0}'.format(content[0]))
					score = fscore.read().strip('\n')
					showinfo = [content[0], '0', '0', content[1], '1', type, score]
					ret.append(showinfo)
		else:
			# show selected commit
			checkCommitID = False
			with open("../dataBase/candidates") as f:
				lines = f.readlines()
				for line in lines:
					content = line.strip("\n").split()
					if len(content) != 2:
						print("OQServer ERROR: candidates format error")
						continue
					if commitID == content[0]:
						checkCommitID = True
						break
			showinfo = None
			if checkCommitID == False:
				showinfo = ['0', 'No details.', 'No details.', '0', '0', '0', '0']
			else:
				detail = os.popen('bash get_commit_detail.sh {0}'.format(commitID))
				comment = os.popen('bash get_commit_comment.sh {0}'.format(commitID))
				showinfo = ['0', detail, comment, '0', '0', '0', '0']
			ret.append(showinfo)
		return ret
	with open("../dataBase/candidates") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 2:
				print("OQServer ERROR: candidates format error")
				continue
			ftype = os.popen('bash get_type.sh {0}'.format(content[0]))
			type = ftype.read().strip('\n')
			fscore = os.popen('bash get_score.sh {0}'.format(content[0]))
			score = fscore.read().strip('\n')
			showinfo = [content[0], '0', '0', content[1], '0', type, score]
			ret.append(showinfo)
	with open("../dataBase/frozen.usr") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 3:
				print("OQServer ERROR: frozen.usr format error")
				continue
			for i in ret:
				if i[0] == content[0] and user == content[2]:
					i[3] = '1'
	record(user, "Show commitIDs")
	return ret

def lockShow(user, commitID, selected):
	flock()
	ret = show(user, commitID, selected)
	funlock()
	return ret

def history(user):
	return getRecord(user)

def lockHistory(user):
	flock()
	ret, __history = history(user)
	funlock()
	return ret, __history

def comment(user, commitID, __content):
	checkCommit = False
	if len(__content) == 0:
		return -1
	with open("../dataBase/candidates") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 2:
				print("OQServer ERROR: candidates format error")
				continue
			if commitID == content[0]:
				checkCommit = True
				break
	if checkCommit == False:
		return -1
	commentBody = "{0} 说：\n{1}\n".format(user, content)
	with open("../dataBase/comments/{0}", 'a+') as f:
		f.write(commentBody)
	record(user, "Comment {0}".format(commitID))
	return 0

def lockComment(user, commitID, content):
	flock()
	ret = comment(user, commitID, content)
	funlock()
	return ret

