import sys
import os
workHome = os.getenv('CWORKON_HOME')
if workHome not in sys.path:
	sys.path.append(workHome)
import dist_client
import re
import time

def help():
	print('\033[0;44;43m简介:\033[0m')
	print(' openEuler kernel问题分发系统，使用前请先配置git的user.email，使用下面指令您可以认领某几个问题，')
	print(' 在此期间该问题为你所有，有效期维持两天，如果有效期内您向openEuler推送解决该问题的补丁，且合入')
	print(' 到openEuler仓库内，您将获得我们赠送的积分，若积分排名靠前您还会收到我们社区送出的礼品。')
	print(' 挑选问题的规则如下：')
	print(" 1、LTS或LTS[C]类型的问题，只能认领一个，且如果您解决了该类型问题，后续也将不能再认领这种类型的问题;")
	print(" 2、BUG类型的问题，每个有效期（2天）之内最多只能认领2个，如果您因为任何原因放弃解决认领的问题，请及时释放!")
	print(" 3、COURSE类型问题，暂不做限制。")
	print('\033[0;37;44m指令:\033[0m')
	print(' # Question show                     //显示所有待解决的问题，bugzilla为记录该问题的数据库地址，Claimed表示是否已被人认领')
	print(' # Question show {commitID}          //显示该问题的详细信息包括评论，\033[1m输入一个commitID，输入时候{}要去掉\033[0m')
	print(' # Question show {commitID} detail   //显示该问题的详细信息')
	print(' # Question show {commitID} comment  //显示该问题的评论')
	print(' # Question show claimd              //显示你认领的问题')
	print(' # Question claim                    //随机认领一个问题')
	print(' # Question claim {type}             //随机认领一个type类型的问题，type可以为LTS,LTS[C],BUG,COURSE，\033[1m输入时{}去掉，注意[]转义\033[0m')
	print(' # Question claim {commitID}         //认领你想要解决的问题')
	print(' # Question hang {commitID}          //释放你认领的问题')
	print(' # Question comment {commitID}       //对问题进行评论，按ctrl+D结束输入')
	print(' # Question history                  //查询你的操作记录')
	print('\033[0;37;44m提示:\033[0m')
	print('问题列表中会显示该问题的积分(score)，本应用用于openEuler kernel社区交流Linux技术问题，严禁从事其他无关活动!')
	print('查看积分排名的网址：www.xxx.com')
	print('规则详情请参考：www.xxx.com')
	print('\n\033[1;37mCopyright © Bobo \033[0m')
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
			result = dist_client.distClient_Show(email, '0', '0')
			result_filter = result
		elif len(argv) == 3:
			if argv[2] == 'claimed':
				result = dist_client.distClient_Show(email, '0', 'selected')
				for r in result:
					result_filter.append(r)
			else:
				# input is commitID
				result = dist_client.distClient_Show(email, argv[2], '0')
				if len(result) != 0:
					print(result[0][1])
					print("\033[0;37;44m评论区:\033[0m\n{0}".format(result[0][3]))
				exit(0)
		elif len(argv) == 4:
			if argv[3] == 'detail':
				result = dist_client.distClient_Show(email, argv[2], '0')
				if len(result) != 0:
					print(result[0][1])
			elif argv[3] == 'comment':
				result = dist_client.distClient_Show(email, argv[2], '0')
				if len(result) != 0:
					print("\033[0;37;44m评论区:\033[0m\n{0}".format(result[0][3]))
			else:
				help()
			exit(0)
		else:
			help()

		for rf in result_filter:
			print("commitID:{0[0]} bugzilla:{0[2]} claimed:{0[4]} type:{0[5]} \033[1mscore:{0[6]}\033[0m".format(rf))
		exit(0)

	if argv[1] == 'claim':
		if len(argv) == 2:
			result = dist_client.distClient_Select(email, '0')
		elif len(argv) == 3:
			result = dist_client.distClient_Select(email, argv[2])
		else:
			help()
		if result[0] == '-1':
			if len(argv) == 2:
				print("["+time.asctime(time.localtime(time.time()))+"]"+" Random claim failed")
			if len(argv) == 3:
				print("["+time.asctime(time.localtime(time.time()))+"]"+" Fail to claim commitID:{0}".format(argv[2]))
		else:
			print("["+time.asctime(time.localtime(time.time()))+"]"+" Success claim: commitID:{0[0]}, bugzilla:{0[1]}".format(result))
		exit(0)

	if argv[1] == 'hang':
		if len(argv) != 3:
			help()
		result = dist_client.distClient_Cancel(email, argv[2])
		if result == 0:
			print("["+time.asctime(time.localtime(time.time()))+"]"+" Failed to hang commitID:{0}".format(argv[2]))
		else:
			print("["+time.asctime(time.localtime(time.time()))+"]"+" Success hang: commitID:{0}".format(argv[2]))
		exit(0)
	if argv[1] == 'history':
		if len(argv) != 2:
			help()
		result, history = dist_client.distClient_History(email)
		if result == 0:
			print(history.strip('\n'))
		else:
			print("["+time.asctime(time.localtime(time.time()))+"]"+" Fail to search your processing history")
		exit(0)
	if argv[1] == 'comment':
		if len(argv) != 3:
			help()
		no_of_lines = 20
		lines = ""
		for line in sys.stdin:
			lines += line
		result = dist_client.distClient_Comment(email, argv[2], lines)
		if result == 0:
			print("["+time.asctime(time.localtime(time.time()))+"]"+" Success to comment")
		else:
			print("["+time.asctime(time.localtime(time.time()))+"]"+" Fail to comment")
		exit(0)
	help()
