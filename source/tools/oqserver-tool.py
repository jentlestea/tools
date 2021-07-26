import sys
import fcntl
import os
workOnTools = os.getenv('WORKON_HOME') + '/tools'
#oqserver-tool reflush
#oqserver-tool import

LOCKPATH = workOnTools+"/../dataBase/.lockf"
flockfd = None
#workOnHome = os.getenv('WORKON_HOME')

def flock():
	global flockfd
	flockfd = open(LOCKPATH, 'w+')
	fcntl.flock(flockfd, fcntl.LOCK_EX)
def funlock():
	global flockfd
	fcntl.flock(flockfd, fcntl.LOCK_UN)

def help():
	print('Usage:')
	print('# oqserver-tool reflush-database')
	print('# oqserver-tool import-question {path}')
	exit(0)

if __name__ == '__main__':
	argv = sys.argv
	if len(argv) < 2:
		help()
	if argv[1] == 'reflush-database':
		flock()
		f = os.popen("bash -x "+workOnTools+"/../script/flushPatch.sh")
		err = f.read().strip('\n')
		if err != '0':
			print('ERROR: flush database failed')
		else:
			print('SUCCESS: flush database')
		funlock()
		exit(0)
	if argv[2] == 'import-quesiton':
		if 
		f = os.popen("bash -x "+workOnTools+"/tools/import_question.sh")
		err = f.read().strip('\n')
		if err != '0':
			print('ERROR: import question failed')
		else:
			print('SUCCESS: import question')
		exit(0)
	exit(0)
