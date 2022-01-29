from concurrent import futures
import grpc
import sys
import threading
import socket

import keyValueStore_pb2
import keyValueStore_pb2_grpc

class KeyValueStoreServicer(keyValueStore_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, stopEvent, myAddr, isSecondPart):
        self.pairs = {}
        self._stop_event = stopEvent
        self._myAddr = myAddr
        self._isSecondPart = isSecondPart
    
    def Insert(self, keyValuePair, context):
        myResponse = 0
        if keyValuePair.key not in self.pairs:
            self.pairs[keyValuePair.key] = keyValuePair.value
            myResponse = keyValueStore_pb2.FlagResponse(flag=0)
        else:
            myResponse = keyValueStore_pb2.FlagResponse(flag=-1)
        return myResponse
    
    def Query(self, key, context):
        result = ""
        if key.key in self.pairs:
            result = self.pairs[key.key]
        return keyValueStore_pb2.Value(value=result)
    
    def Activate(self, serviceActivation, context):
        if self._isSecondPart:
            with grpc.insecure_channel(serviceActivation.serverAddr) as newChannel:
                stub = keyValueStore_pb2_grpc.CentralServerStub(newChannel)
                pairServer = keyValueStore_pb2.PairServer()
                pairServer.serverAddr = self._myAddr
                keysMessageList = []
                for key in list(self.pairs.keys()):
                    pairServer.keys.add().key=key
                response = stub.Register(pairServer)
                return keyValueStore_pb2.FlagResponse(flag=response.pairsCount)
        else:
            return keyValueStore_pb2.FlagResponse(flag=0)
    
    def Stop(self, stopParams, context):
        self._stop_event.set()
        return keyValueStore_pb2.FlagResponse(flag=0)

def server(serverPort, isSecondPart):
    stop_event = threading.Event()
    myAddr = f"{socket.getfqdn()}:{str(serverPort)}"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    keyValueStore_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStoreServicer(stop_event, myAddr, isSecondPart), server)
    server.add_insecure_port(f'[::]:{serverPort}')
    server.start()
    stop_event.wait()
    server.stop(grace=1)

if __name__ == '__main__':
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        exit()

    isSecondPart = False
    if len(sys.argv) == 3:
        isSecondPart = True
    serverPort = sys.argv[1]

    server(serverPort, isSecondPart)