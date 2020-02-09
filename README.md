# Usage

## Server side
```python
# First import RPC_Server
from RPC_SERVER import RPC_Server
# Define the function that you want to be invoked remotely
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
# Create Object Of RPC SERVER
Rpc = RPC_Server()
# register_function(func) is used to publish a function that could be obtained by the clients.
Rpc.register(add)
Rpc.register(sub)
Rpc.register(is_hello)
Rpc.register(div)
# Now Bind The Services
Rpc.rebind()
```


## Client side
```python
# First import RPC
from RPC_CLIENT import RPC

# craete instance of RPC
a = RPC()

# The available functions can be called just like a local function
print(a.add(12,1))
print(a.sub(12,1))
print(a.div(12,5))
print(a.is_hello("hello"))
print(a.is_hello("danish"))
```
