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
        """
        Registers key-serverId pairs.
        """
        serverAddr = pairServer.serverAddr
        #If pair server has already sent its keys once or if it is it's first time and
        #we aren't saving keys from more than 10 (self._maxServers) servers already 
        if serverAddr in self._serversAddr or len(self._serversAddr) <= self._maxServers:
            
            #If it is the first time, save the servers id
            if serverAddr not in self._serversAddr:
                self._serversAddr.append(serverAddr)

            #Registers it's keys
            for key in pairServer.keys:
                self._pairs[key.key] = serverAddr

            return keyValueStore_pb2.PairCount(pairsCount=len(pairServer.keys))
        else:        
            return keyValueStore_pb2.PairCount(pairsCount=0)
    
    def MapToServer(self, key, context):
        """
        Returns the servers ID that owns the key. Empty if there are no servers that owns the key.
        """
        result = ""

        if key.key in self._pairs:
            result = self._pairs[key.key]
        
        return keyValueStore_pb2.ServerAddr(serverAddr = result)
    

    def StopCentralServer(self, stopParams, context):
        """
        Stops this server
        """
        self._stop_event.set()
        numKeys = len(self._pairs.keys())
        return keyValueStore_pb2.PairCount(pairsCount=numKeys)

def runServer(serverPort):
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    keyValueStore_pb2_grpc.add_CentralServerServicer_to_server(
        CentralServerServicer(stop_event), server)
    server.add_insecure_port(f'[::]:{serverPort}')
    server.start()
    stop_event.wait()
    server.stop(grace=1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()

    serverPort = sys.argv[1]
    runServer(serverPort)