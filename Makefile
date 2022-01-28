compileProto:
	python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/keyValueStore.proto

run_cli_pares: 
	python client.py $(arg)

run_serv_pares_1: 
	python server.py $(arg)

clean:
