import grpc
import sys

import keyValueStore_pb2
import keyValueStore_pb2_grpc

def firstPartOpts(channel):
    stub = keyValueStore_pb2_grpc.KeyValueStoreStub(channel)
    while(True):

        #Gets user input
        command = input()
        inputSplit = command.split(',')

        #Treat options
        if inputSplit[0] == 'I':
            response = stub.Insert(keyValueStore_pb2.KeyValuePair(key=int(inputSplit[1]), value=inputSplit[2]))
            print(str(response.flag))
        elif inputSplit[0] == 'C':
            response = stub.Query(keyValueStore_pb2.Key(key=int(inputSplit[1])))
            print(str(response.value))
        elif inputSplit[0] == 'A':
            response = stub.Activate(keyValueStore_pb2.ServerAddr(serverAddr=inputSplit[1]))
            print(str(response.flag))
        elif inputSplit[0] == 'T':
            response = stub.Stop(keyValueStore_pb2.StopParams())
            print(str(response.flag))
            if response.flag == 0:
                break

def secondPartOpts(channel):
    stub = keyValueStore_pb2_grpc.CentralServerStub(channel)
    while(True):

        #Gets user input
        command = input()
        inputSplit = command.split(',')

        #Treat options
        if inputSplit[0] == 'C':
            response = stub.MapToServer(keyValueStore_pb2.Key(key=int(inputSplit[1])))
            
            #If there is a server that owns the target key
            if(response.serverAddr != ""):
                pairServerAddr = response.serverAddr

                #Connects to that server and requests the key's value
                with grpc.insecure_channel(pairServerAddr) as channel:
                    secStub = keyValueStore_pb2_grpc.KeyValueStoreStub(channel)
                    response = secStub.Query(keyValueStore_pb2.Key(key=int(inputSplit[1])))
                    print(pairServerAddr+":"+str(response.value))

        elif inputSplit[0] == 'T':
            response = stub.StopCentralServer(keyValueStore_pb2.StopParams())
            print(response.pairsCount)
            break


def runClient(serverAdd, isSecondPart):
    with grpc.insecure_channel(serverAdd) as channel:
        if not isSecondPart:
            firstPartOpts(channel)
        else:
            secondPartOpts(channel)
            

if __name__ == '__main__':
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        exit()

    isSecondPart = False
    if len(sys.argv) == 3:
        isSecondPart = True
    
    serverAdd = str(sys.argv[1])
    runClient(serverAdd, isSecondPart)
