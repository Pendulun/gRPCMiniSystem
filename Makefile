PROTONAME:= keyValueStore
PB2:= $(PROTONAME)_pb2.py
PB2GRPC:= $(PROTONAME)_pb2_grpc.py
PYTHON:=python3

compileProto:
	@$(PYTHON) -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/$(PROTONAME).proto

run_cli_pares: compileProto
	$(PYTHON) client.py $(arg)

run_serv_pares_1: compileProto
	$(PYTHON) server.py $(arg)

run_serv_pares_2: compileProto
	$(PYTHON) server.py $(arg) 1

run_serv_central: compileProto
	$(PYTHON) centralServer.py $(arg)

run_cli_central: compileProto
	$(PYTHON) client.py $(arg) 1

clean:
	rm $(PB2) $(PB2GRPC)