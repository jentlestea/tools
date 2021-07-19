from concurrent import futures
import time
import grpc
import sys
import os
workProtoHome = os.getenv('WORKON_HOME') + '/gRPC/proto'
if workProtoHome not in sys.path:
	sys.path.append(workProtoHome)
import dist_pb2
import dist_pb2_grpc
import process

class dist(dist_pb2_grpc.distServicer):
	def distSelect(self, request, context):
		user = request.user
		commitID = request.commitID
		result = process.lockSelect(user, commitID)
		grpcResult = dist_pb2.Select(commitID = result[0], bugzilla = result[1])
		return grpcResult
	def distCancel(self, request, context):
		user = request.user
		commitID = request.commitID
		ret = process.lockCancel(user, commitID)
		return dist_pb2.Result(result = ret)
	def distShow(self, request, context):
		user = request.user
		commitID = request.commitID
		selected = request.selected
		result = process.lockShow(user, commitID, selected)
		for i in result:
			grpcResult = dist_pb2.Show(commitID = i[0], bugzilla = i[1], user = i[2], type = i[3], score = i[4])
			yield grpcResult
	def distHistory(self, request, context):
		user = request.user
		ret, __history = process.lockHistory(user)
		return dist_pb2.History(result = ret, history = __history)

def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	dist_pb2_grpc.add_distServicer_to_server(dist(), server)
	server.add_insecure_port('[::]:50051')
	server.start()
	process.prepare()
	print('[dist Service] startup [OK]')
	try:
		while True:
			process.flock()
			print('[dist Service] Waiting for flush patches...')
			f = os.popen("bash ../script/flushPatch.sh")
			err = f.read().strip('\n')
			if err != '0':
				print("[dist Service] Flush patches failed!")
				process.clean()
				server.stop(0)
				process.funlock()
				exit(0)
			print("[dist Service] Flush patches success!")
			process.funlock()
			time.sleep(60*60*24) # one day in seconds
	except KeyboardInterrupt:
		process.clean()
		server.stop(0)

if __name__ == '__main__':
	workHome = os.getenv('WORKON_HOME') + '/gRPC'
	os.chdir(workHome)
	serve()
