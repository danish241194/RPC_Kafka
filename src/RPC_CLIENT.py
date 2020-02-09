from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import dumps
from json import loads
from time import sleep

class RPC:
	def __init__(self):

		self.servername = "servername11"
		self.clientname = "clientname11"
		self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		self.consumer = KafkaConsumer(self.clientname,bootstrap_servers=['localhost:9092'], auto_commit_interval_ms=10,auto_offset_reset='earliest',enable_auto_commit=True,group_id=self.clientname,value_deserializer=lambda x: loads(x.decode('utf-8')))

	def __getattr__(self, name):
		def wrapper(*args):
			packet = self.create_final_packet(name,args)
			self.producer.send(self.servername, value=packet)
			for message in self.consumer:
				message = message.value
				ans = self.string_to_type(message["type"],message["value"])
				self.consumer.commit()
				break

			return ans
		return wrapper

	def create_final_packet(self,function_name,args):
			parameters = self.create_packet_of_params(args)
			packet = {"function":function_name,
				"parameters":parameters
				}
			return packet

	def create_packet_of_params(self,args):
		parameters = {}
		for idx, param in enumerate(args):
			parameters["type"+f"{idx}"] = self.type_to_string(type(param))
			parameters["value"+f"{idx}"] = str(param)
		return parameters

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


