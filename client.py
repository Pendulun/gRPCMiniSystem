import grpc
import sys
sys.path.append('protos')

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
            elif inputSplit[0] == 'C':
                pass
            elif inputSplit[0] == 'A':
                pass
            elif inputSplit[0] == 'T':
                pass
            elif inputSplit[0] == 'K':
                break

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()

    serverAdd = sys.argv[1]
    runClient(serverAdd)
