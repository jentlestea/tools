import os
import random
import fcntl
import time
import _thread

LOCKPATH = "../dataBase/.lockf"
flockfdMap = {}
#workOnHome = os.getenv('WORKON_HOME')

def flock(user):
	global flockfdMap
	flockfd = open(LOCKPATH, 'w+')
	flockfdMap[user] = flockfd
	fcntl.flock(flockfd, fcntl.LOCK_EX)
def funlock(user):
	global flockfdMap
	fcntl.flock(flockfdMap[user], fcntl.LOCK_UN)
	flockfdMap[user].close()
	del flockfdMap[user]

def prepare():
	try:
		_thread.start_new_thread(lockClearFrozen, ())
	except:
		print('ERROR: create clear frozen thread failed')

def clean():
	return

lockTimeMap = {}
def setFrozen(commitID):
	global lockTimeMap
	currentTime = time.time()
	lockTimeMap[commitID] = currentTime

#2 day frozen
frozenTime = 60*60*24*2
def lockClearFrozen():
	flock('frozen')
	currentTime = time.time()
	lines = None
	with open("../dataBase/frozen.usr") as f:
		lines = f.readlines()
	with open("../dataBase/frozen.usr", 'w+') as f:
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 3:
				return ret
			if content[0] not in lockTimeMap:
				print("ERROR: {0} not found when clear frozen".format(content[0]))
				continue
			div = currentTime - lockTimeMap[content[0]]
			if div < frozenTime:
				f.write("{0[0]} {0[1]} {0[2]}\n".format(content))
			else:
				del lockTimeMap[content[0]]
		f.flush()
	funlock('frozen')
	time.sleep(60*60)

def record(user, line):
	path = "../dataBase/person/{0}".format(user)
	with open(path, 'a+') as f:
		f.write("["+time.asctime(time.localtime(time.time()))+"] "+"{0}\n".format(line))
		f.flush()

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
		frozens = []
		with open("../dataBase/frozen.usr") as f:
			lines = f.readlines()
			for line in lines:
				lineStrip = line.strip('\n').split()
				if len(lineStrip) != 3:
					print('OQServer ERROR: frozen.usr format error')
					continue
				frozens.append(lineStrip[0])
		for c in contents:
			ftype = os.popen("bash get_type.sh {0}".format(c[0]))
			type = ftype.read.strip('\n')
			if type.find('LTS') != -1 and lockLTS == True:
				continue
			if c[0] in frozens:
				continue
			ret = c
			break
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
			f.flush()
		setFrozen(ret[0])
		record(user, "Claim commitID:{0}".format(ret[0]))
	return ret

def lockSelect(user, commitID):
	flock(user)
	ret = select(user, commitID)
	funlock(user)
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
		f.flush()
	if found == 1:
		record(user, "hang commitID:{0}".format(commitID))
	return found

def lockCancel(user, commitID):
	flock(user)
	ret = cancel(user, commitID)
	funlock(user)
	return ret

def show(user, commitID, selected):
	ret = []
	if commitID != '0' or selected != '0':
		if selected == 'claimed':
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
					showinfo = [content[0], '0', content[1], '0', '1', type, score]
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
				showinfo = ['0', 'No details.', '0', 'No details.', '0', '0', '0']
			else:
				retDetail = os.popen('bash get_commit_detail.sh {0}'.format(commitID))
				retComment = os.popen('bash get_commit_comment.sh {0}'.format(commitID))
				#print(comment.readlines())
				detail = None
				comment = None
				if retDetail.read().strip('\n') == '0':
					with open(".detailTmp") as f:
						detail = f.read()
				else:
					detail = "No details."
				if retComment.read().strip('\n') == '0':
					with open(".commentTmp") as f:
						comment = f.read()
				else:
					comment = "No comment."
				showinfo = ['0', detail, '0', comment, '0', '0', '0']
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
			showinfo = [content[0], '0', content[1], '0', '0', type, score]
			ret.append(showinfo)
	with open("../dataBase/frozen.usr") as f:
		lines = f.readlines()
		for line in lines:
			content = line.strip("\n").split()
			if len(content) != 3:
				print("OQServer ERROR: frozen.usr format error")
				continue
			for i in ret:
				if i[0] == content[0]:#and user == content[2]:
					i[4] = '1'
	record(user, "Show commitIDs")
	return ret

def lockShow(user, commitID, selected):
	flock(user)
	ret = show(user, commitID, selected)
	funlock(user)
	return ret

def history(user):
	return getRecord(user)

def lockHistory(user):
	flock(user)
	ret, __history = history(user)
	funlock(user)
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
	commentBody = "{0} 说:\n{1}\n".format(user, __content)
	with open("../dataBase/comments/{0}".format(commitID), 'a+') as f:
		f.write(commentBody)
		f.flush()
	record(user, "Comment {0}".format(commitID))
	return 0

def lockComment(user, commitID, content):
	flock(user)
	ret = comment(user, commitID, content)
	funlock(user)
	return ret

