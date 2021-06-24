import sys
sys.path.append("../")
import dist_client
import os

def help():
	print('Usage:')
	print('# python3 grab.py show')
	print('# python3 grab.py select')
	print('# python3 grab.py select {commitID}')
	print('# python3 grab.py cancel {commitID}')
	exit(0)

if __name__ == '__main__':
	argv = sys.argv
	if len(argv) < 2:
		help()
	f = os.popen("git config --list | grep user.email | sed -n -e 's/.*user.email=\(.*\)/\1/p'")
	email = f.read()
	if email == '':
		print('Please use git config to set your user.email')
		exit(0)

	if argv[1] == 'show':
		if len(argv) != 2:
			help()
		result = dist_client.distClient_Show(email)
		for r in result:
			print("{commitID:0[0], bugzilla:0[1], belongsU:0[2]}".format(r))
		exit(0)

	if argv[2] == 'select':
		if len(argv) == 2:
			result = dist_client.distClient_Select(email, '0')
		elif len(argv) == 3:
			result = dist_client.distClient_Select(email, argv[2])
		else:
			help()
		if result != 0:
			print("Fail")
		else:
			print("Success")
		exit(0)

	if argv[3] == 'cancel':
		if len(argv) != 3:
			help()
		dist_client.distClient_Cancel(email, argv[2])
