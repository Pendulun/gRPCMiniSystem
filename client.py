import grpc
import sys

import keyValueStore_pb2
import keyValueStore_pb2_grpc

def runClient(serverAdd):
    with grpc.insecure_channel(serverAdd) as channel:
        stub = keyValueStore_pb2_grpc.KeyValueStoreStub(channel)
        while(True):
            command = input()
            inputSplit = command.split(',')

            if inputSplit[0] == 'I':
                response = stub.Insert(keyValueStore_pb2.KeyValuePair(key=int(inputSplit[1]), value=inputSplit[2]))
                print(str(response.flag))
            elif inputSplit[0] == 'C':
                response = stub.Query(keyValueStore_pb2.Key(key=int(inputSplit[1])))
                print(str(response.value))
            elif inputSplit[0] == 'A':
                response = stub.Activate(keyValueStore_pb2.ServiceActivation(serviceName=inputSplit[1]))
                print(str(response.flag))
            elif inputSplit[0] == 'T':
                response = stub.Stop(keyValueStore_pb2.StopParams())
                if response.flag == 0:
                    break
            

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()

    serverAdd = str(sys.argv[1])
    runClient(serverAdd)
