import sys
import dist_client
import os
import re

def help():
	print('Usage:')
	print('# Question show')
	print('# Question show selected')
	print('# Question select')
	print('# Question select {commitID}')
	print('# Question cancel {commitID}')
	exit(0)

if __name__ == '__main__':
	argv = sys.argv
	if len(argv) < 2:
		help()
	f = os.popen("git config --list | grep user.email")
	formatEmail = f.read().strip('\n')
	matchEmail = re.match(r'(user.email)=(.*)', formatEmail, re.M|re.I)
	email = matchEmail.group(2).strip('\n')
	if email == '' or email.find('@') == -1:
		print('Please use git config to set your user.email')
		exit(0)

	if argv[1] == 'show':
		result_filter = []
		if len(argv) == 2:
			result = dist_client.distClient_Show(email)
			result_filter = result
		elif len(argv) and argv[2] == 'selected':
			result = dist_client.distClient_Show(email)
			for r in result:
				if r[2] != '1':
					continue
				result_filter.append(r)
		else:
			help()
		for rf in result_filter:
			print("commitID:{0[0]} bugzilla:{0[1]} ACK:{0[2]} type:{0[3]} score:{0[4]}".format(rf))
		exit(0)

	if argv[1] == 'select':
		if len(argv) == 2:
			result = dist_client.distClient_Select(email, '0')
		elif len(argv) == 3:
			result = dist_client.distClient_Select(email, argv[2])
		else:
			help()
		if result[0] == '-1':
			if len(argv) == 2:
				print("Random selection failed")
			if len(argv) == 3:
				print("Fail to select commitID:", argv[2])
		else:
			print("Success select: commitID:{0[0]}, bugzilla:{0[1]}".format(result))
		exit(0)

	if argv[1] == 'cancel':
		if len(argv) != 3:
			help()
		result = dist_client.distClient_Cancel(email, argv[2])
		if result == 0:
			print("Failed to cancel commitID:", argv[2])
		else:
			print("Success cancel: commitID:", argv[2])
		exit(0)
