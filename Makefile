PROTONAME:= keyValueStore
PB2:= $(PROTONAME)_pb2.py
PB2GRPC:= $(PROTONAME)_pb2_grpc.py

compileProto:
	@python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/$(PROTONAME).proto

run_cli_pares: compileProto
	python client.py $(arg)

run_serv_pares_1: compileProto
	python server.py $(arg)

run_serv_pares_2: compileProto
	python server.py $(arg) 1

run_serv_central: compileProto
	python centralServer.py $(arg)

run_cli_central: compileProto
	python client.py $(arg) 1

clean:
	rm $(PB2) $(PB2GRPC)