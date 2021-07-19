import sys
import os
workProtoHome = os.getenv('CWORKON_HOME') + '/proto'
if workProtoHome not in sys.path:
	sys.path.append(workProtoHome)
import grpc
import dist_pb2
import dist_pb2_grpc

workHome = os.getenv('CWORKON_HOME')
#addr = "139.159.148.89:50051"
f = open(workHome + "/ip.conf")
addr = f.readline().strip('\n')
f.close()
stub = None

def distClient_Connect():
	global stub
	channel = grpc.insecure_channel(addr)
	stub = dist_pb2_grpc.distStub(channel)

def distClient_Select(__user, __commitID):
	global stub
	distClient_Connect()
	response = stub.distSelect(dist_pb2.UsrMsg(user = __user, commitID = __commitID))
	return [response.commitID, response.bugzilla]

def distClient_Cancel(__user, __commitID):
	global stub
	distClient_Connect()
	response = stub.distCancel(dist_pb2.UsrMsg(user = __user, commitID = __commitID))
	return response.result

def distClient_Show(__user):
	global stub
	distClient_Connect()
	result = []
	response = stub.distShow(
		dist_pb2.Usr(user = __user)
	)
	for r in response:
		rr = []
		rr.append(r.commitID)
		rr.append(r.bugzilla)
		rr.append(r.user)
		rr.append(r.type)
		rr.append(r.score)
		result.append(rr)
	return result

def distClient_History(__user):
	global stub
	distClient_Connect()
	response = stub.distHistory(
		dist_pb2.Usr(user = __user)
	)
	return response.result, response.history
