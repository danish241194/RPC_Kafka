from RPC_SERVER import RPC_Server
def add(a,b):
	return a+b
def sub(a,b):
	return a-b
def is_hello(str_):
	if str_=="hello":
		return True
	return False
def div(a,b):
	return a/b

Rpc = RPC_Server()
Rpc.register(add)
Rpc.register(sub)
Rpc.register(is_hello)
Rpc.register(div)
Rpc.rebind()
