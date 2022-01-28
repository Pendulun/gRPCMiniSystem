from concurrent import futures
import grpc
import sys
sys.path.append('protos')

import keyValueStore_pb2
import keyValueStore_pb2_grpc

class KeyValueStoreServicer(keyValueStore_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self.pairs = {}
    
    def Insert(self, keyValuePair, context):
        self.pairs[keyValuePair.key] = keyValuePair.value
        print(list(self.pairs.items()))
        return keyValueStore_pb2.FlagResponse(flag=1)

def server(serverPort):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    keyValueStore_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStoreServicer(), server)
    server.add_insecure_port(f'[::]:{serverPort}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()

    serverPort = sys.argv[1]

    server(serverPort)