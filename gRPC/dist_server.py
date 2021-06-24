from concurrent import futures
import time
import grpc
import sys
import os
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
		process.lockCancel(user, commitID)
		return dist_pb2.Result(result = 0)
	def distShow(self, request, context):
		user = request.user
		result = process.lockShow(user)
		for i in result:
			grpcResult = dist_pb2.Show(commitID = result[0], bugzilla = result[1], user = result[2])
			yield grpcResult

def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	dist_pb2_grpc.add_distServicer_to_server(dist(), server)
	server.add_insecure_port('[::]:50051')
	server.start()
	print('[dist Service] startup [OK]')
	try:
		while True:
			f = os.popen("sh ../script/flushPatch.sh")
			err = f.read().strip('\n')
			if err != '0':
				print("Flush patches failed!")
			time.sleep(60*60*24) # one day in seconds
	except KeyboardInterrupt:
		server.stop(0)

if __name__ == '__main__':
	workhome = os.getenv('WORKON_HOME') + '/gRPC'
	os.chdir(workhome)
	serve()