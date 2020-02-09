from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import loads
from json import dumps

class RPC_Server:
	def __init__(self):
		self.servername = "servername11"
		self.clientname = "clientname11"
		self.registered_functions = {}
		self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		self.consumer = KafkaConsumer(self.servername,bootstrap_servers=['localhost:9092'],auto_offset_reset='earliest',enable_auto_commit=True,group_id=self.servername, auto_commit_interval_ms=100,value_deserializer=lambda x: loads(x.decode('utf-8')))
	def register(self,function_ref):
		self.registered_functions[function_ref.__name__] = function_ref
		
	def rebind(self):
		while(True):
			for message in self.consumer:
				message = message.value
				function,parameter_list = self.get_function(message)
				result = function(*parameter_list)
				print(result)
				return_type = self.type_to_string(result)
				packet = {"type":return_type,
					"value":result						
					}
				self.producer.send(self.clientname,value = packet)

	def get_function(self,message):
		function_name  = message["function"]
		print(function_name)
		parameter_json = message["parameters"]
		parameters_list = []
		for i in range(int(len(parameter_json)/2)):
			key = "type"+str(i)
			value = "value"+str(i)
			type_ = parameter_json[key]
			value_ = parameter_json[value]
			value_ = self.string_to_type(type_,value_)
			parameters_list.append(value_)
		return self.registered_functions[function_name] , parameters_list

	def type_to_string(self,type_):
		if(type_==int):
			return "int"
		elif(type_==float):
			return "float"
		elif(type_==bool):
			return "bool"
		elif(type_==str):
			return "str"

		return "str"
	def string_to_type(self,type_,value):
		if(type_=="int"):
			return int(value)
		elif(type_=="float"):
			return float(value)
		elif(type_=="bool"):
			return bool(value)
		return value


