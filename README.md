# gRPCMiniSystem

## Compile .proto

make compileProto

## Run pairs server with simple activation

make run_serv_pares_1 arg=portToUse

## Run client that communicates with pairs servers

make run_cli_pares arg=serverIP:serverPort

## Run pairs server that communicates with central server

make run_serv_pares_2 arg=portToUse

## Run central server

make run_serv_central arg=portToUse

## Run client that communicates with central server

make run_cli_central arg=centralServerIp:centralServerPort

Every rule depends on the Compile .proto rule.