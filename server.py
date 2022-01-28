from concurrent import futures
import grpc
import sys
import threading
import socket

import keyValueStore_pb2
import keyValueStore_pb2_grpc

class KeyValueStoreServicer(keyValueStore_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, stopEvent, myAddr):
        self.pairs = {}
        self._stop_event = stopEvent
        self._myAddr = myAddr
    
    def Insert(self, keyValuePair, context):
        myResponse = 0
        if keyValuePair.key not in self.pairs:
            self.pairs[keyValuePair.key] = keyValuePair.value
            myResponse = keyValueStore_pb2.FlagResponse(flag=0)
        else:
            myResponse = keyValueStore_pb2.FlagResponse(flag=-1)
        print(list(self.pairs.items()))
        return myResponse
    
    def Query(self, key, context):
        result = ""
        if key.key in self.pairs:
            result = self.pairs[key.key]
        return keyValueStore_pb2.Value(value=result)
    
    def Activate(self, serviceActivation, context):
        with grpc.insecure_channel(serviceActivation.serverAddr) as newChannel:
            print("Conectou com central!")
            stub = keyValueStore_pb2_grpc.CentralServerStub(newChannel)
            pairServer = keyValueStore_pb2.PairServer(serverAddr = self._myAddr)
            pairServer.keys.extend(list(self.pairs.keys()))
            response = stub.Register(pairServer)
            print(f"response: {response.pairsCount}")
            return keyValueStore_pb2.FlagResponse(flag=response.pairsCount)
    
    def Stop(self, stopParams, context):
        self._stop_event.set()
        return keyValueStore_pb2.FlagResponse(flag=0)

def server(serverPort):
    stop_event = threading.Event()
    myAddr = socket.getfqdn()+str(serverPort)
    print(f"My Addr: {myAddr}")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    keyValueStore_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStoreServicer(stop_event, myAddr), server)
    server.add_insecure_port(f'[::]:{serverPort}')
    server.start()
    stop_event.wait()
    server.stop(grace=None)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()

    serverPort = sys.argv[1]

    server(serverPort)