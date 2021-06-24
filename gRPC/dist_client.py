import sys
import grpc
import dist_pb2
import dist_pb2_grpc

addr = "139.159.148.89"
stub = None

def distClient_Connect():
    global stub
    channel = grpc.insecure_channel(addr)
    stub = qosos_pb2_grpc.distStub(channel)

def distClient_Select(__user, __commitID):
    distClient_Connect()
    response = stub.distSelect(dist_pb2.UsrMsg(user = __user, commitID = __commitID))
    return response.commitID, response.bugzilla

def distClient_Cancel(__user, __commitID):
    distClient_Connect()
    response = stub.distCancel(dist_pb2.UsrMsg(usr = __user, commitID = __commitID))
    return response.result

def distClient_Show(__user):
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
        result.append(rr)
    return result