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
		f = os.popen("bash "+workOnTools+"/../script/flushPatch.sh")
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
		flock()
		f = os.popen("bash "+workOnTools+"/importfs/ifscan.sh")
		err = f.read().strip('\n')
		if err != '0':
			print('ERROR: push repo failed')
		else:
			print('SUCCESS: pls check ./import.csv.tmp')
		funlock()
		exit(0)
	if argv[1] == 'import-csv':
		if len(argv) != 3:
			help()
		flock()
		if os.path.exists(commitFile) == True:
			f = os.popen("cp "+commitFile+" "+commitFile+".old")
			err = f.read().strip('\n')
			if err != '':
				print(err,'ERROR: backend import csv failed')
		f = os.popen("bash checkcsv.sh {0}".format(argv[2]))
		err = f.read().strip('\n')
		if err != '0':
			print('ERROR: pls check csv format!')
			exit(0)
		f = os.popen("cp "+argv[2]+" "+commitFile+"")
		err = f.read().strip('\n')
		if err != '':
			print(err,'ERROR: import csv failed')
		else:
			print('SUCCESS: now you can run reflush-database!')
		funlock()
		exit(0)
	help()
