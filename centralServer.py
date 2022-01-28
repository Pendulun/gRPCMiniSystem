from concurrent import futures
import grpc
import sys
import threading

import keyValueStore_pb2
import keyValueStore_pb2_grpc

class CentralServerServicer(keyValueStore_pb2_grpc.CentralServerServicer):
    def __init__(self, stopEvent):
        self._pairs = {}
        self._serversAddr = []
        self._stop_event = stopEvent
        self._maxServers = 10
    
    def Register(self, pairServer, context):
        serverAddr = pairServer.serverAddr
        print(f"Recebeu msg do server {serverAddr}")
        if serverAddr in self._serversAddr or len(self._serversAddr) <= self._maxServers:
            
            if serverAddr not in self._serversAddr:
                self._serversAddr.append(serverAddr)

            for key in pairServer.keys:
                self._pairs[key.key] = serverAddr

            print(list(self._pairs.items()))
        else:        
            return keyValueStore_pb2.PairCount(pairsCount=0)
    
    def MapToServer(self, key, context):
        result = ""

        if key.key in self._pairs:
            result = self._pairs[key.key]
        
        return keyValueStore_pb2.ServerAddr(serverAddr = result)
    

    def StopCentralServer(self, stopParams, context):
        self._stop_event.set()
        numKeys = len(self.pairs.keys())
        return keyValueStore_pb2.PairCount(pairsCount=numKeys)

def server(serverPort):
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    keyValueStore_pb2_grpc.add_CentralServerServicer_to_server(
        CentralServerServicer(stop_event), server)
    server.add_insecure_port(f'[::]:{serverPort}')
    server.start()
    stop_event.wait()
    server.stop(grace=None)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()

    serverPort = sys.argv[1]
    server(serverPort)