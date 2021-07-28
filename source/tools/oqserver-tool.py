import sys
import fcntl
import os
workOnTools = os.getenv('WORKON_HOME') + '/tools'
#oqserver-tool reflush
#oqserver-tool import

LOCKPATH = workOnTools+"/../dataBase/.lockf"
flockfd = None
#workOnHome = os.getenv('WORKON_HOME')

commitFile=os.getenv('IMPORT_COMMIT_FILE')

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
	print('# oqserver-tool push-repo')
	print('# oqserver-tool import-csv {csv_path}')
	exit(0)

if __name__ == '__main__':
	argv = sys.argv
	if len(argv) < 2:
		help()
	if argv[1] == 'reflush-database':
		if len(argv) != 2:
			help()
		flock()
		f = os.popen("bash -x "+workOnTools+"/../script/flushPatch.sh")
		err = f.read().strip('\n')
		if err != '0':
			print('ERROR: flush database failed')
		else:
			print('SUCCESS: flush database')
		funlock()
		exit(0)
	if argv[1] == 'push-repo':
		if len(argv) != 2:
			help()
		f = os.popen("bash -x "+workOnTools+"/tools/importfs/ifscan.sh")
		err = f.read().strip('\n')
		if err != '0':
			print('ERROR: import scan failed')
		else:
			print('SUCCESS: import scan, check ./import.csv.tmp')
		exit(0)
	if argv[1] == 'import-csv':
		if len(argv) != 3:
			help()
		f = os.popen("cp "+commitFile+" "+commitFile+".old")
		err = f.read().strip('\n')
		if err != '0':
			print('ERROR: backend import csv failed')
		f = os.popen("cp "+argv[2]+" "+commitFile+"")
		err = f.read().strip('\n')
		if err != '0':
			print('ERROR: import csv failed')
		else:
			print('SUCCESS: now you can run reflush-database!')
		exit(0)
	help()
