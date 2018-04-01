import socket;
import threading;
import subprocess;
import shlex;
import zlib;
import pkg_resources;
import incendium.data as data;
import incendium.messages as msg;
import io;
import os.path;
from select import select;

HANDSHAKE_MESSAGE_NONE=-1;
HANDSHAKE_MESSAGE_ERROR_STRING=0;
HANDSHAKE_MESSAGE_SUCCESS=1;
HANDSHAKE_MESSAGE_DISPLAY_STRING=2;
HANDSHAKE_MESSAGE_WAIT_IN_LINE=3;
HANDSHAKE_MESSAGE_LINE_TOO_LONG=4;
HANDSHAKE_MESSAGE_PASSWORD_CHALLENGE=5;

def SIMPLE_FORWARD(client,message):
	"""
	Transfer function that simply forwards the messages with no change.
	
	This is the default value for the client's transfer functions.
	"""
	if isinstance(message,(msg.Message,msg.Command)):
		return [message];
	else:
		return message;
		
def _pack_message(message_data,compress=False):
	"""
	Wraps a message with a size and compression field header.
	
	This function will always use compression if the compress-argument is set to True.
	It will also use compression if the length of message_data is larger than 65535.
	"""
	length=len(message_data);
	if length>0xffff or compress:
		message_data=zlib.compress(message_data);
		length=len(message_data);
		if length>0xffffff:
			#TODO throw error
			pass;
		packet=bytearray(3);
		packet[0]=(length>>16) & 0xff;
		packet[1]=(length>>8) & 0xff;
		packet[2]=length & 0xff;
		packet+=message_data;
		return packet;
	else:
		packet=bytearray(3);
		packet[0]=0xff;
		packet[1]=(length>>8) & 0xff;
		packet[2]=length & 0xff;
		packet+=message_data;
		return packet;

def _unpack_message(packet):
	"""
	Extracts the message data from the raw data packet.
	"""
	message_data=packet[3:];
	if packet[0]!=0xff:
		message_data=zlib.decompress(message_data); #TODO check if actually compressed
	return message_data;
	
def _connection_loop(client,to_server):
	while client.connected:
		try:
			if to_server:
				select([client.conn_client],[],[]);
				message_data=_read_message(client.conn_client);
			else:
				select([client.conn_server],[],[]);
				message_data=_read_message(client.conn_server);
			if message_data==None:	#Connection aborted
				break;
		except ConnectionError as cerr:
			print(cerr);
			break;
		func=client.on_data_to_server if to_server else client.on_data_to_client;
		message_data=func(client,message_data);
		message_data=_unpack_message(message_data);
		
		stream=io.BytesIO(message_data);
		message=data.read_message(stream);
		
		func=client.on_message_to_server if to_server else client.on_message_to_client;
		processed_messages=func(client,message);
		
		for m in processed_messages:
			if isinstance(m,(msg.FrameNoInfo,msg.FrameWithInfo,msg.UserInput)):
				processed_commands=[];
				for cmd in m.command_list:
					func=client.on_command_to_server if to_server else client.on_command_to_client;
					processed_commands+=func(client,cmd);
				m.command_list=processed_commands;
				
			if to_server:
				client.send_to_server(m);
			else:
				client.send_to_client(m);
	client.connected=False;
		
def _read_message(sock):
	"""
	Fetches a single message from the input socket.
	"""
	size_data=sock.recv(1);
	if len(size_data)==0: #EOF
		return None;
	while len(size_data)<3:
		size_data+=sock.recv(1);
	size=0;
	if size_data[0]!=0xff:
		size=(size_data[0]<<16)+(size_data[1]<<8)+size_data[2];
	else:
		size=(size_data[1]<<8)+size_data[2];
	#print("Size"+size);
	message=b"";
	bytes_received=0;
	while bytes_received<size:
		data=sock.recv(min(4096,size-bytes_received));
		message+=data;
		bytes_received+=len(data);
	return size_data+message;
	
def _connect(client):
	"""
	Establishes the connection between client and server.
	"""
	server=socket.socket();
	server.bind(("localhost",client.local_port));
	server.listen();
	select([server],[],[]);
	client.conn_client=server.accept()[0]; #TODO save address
	
	client.conn_server=socket.socket();
	client.conn_server.connect(("192.99.201.128",21103));
	
	_send_handshake(client);
	_receive_handshake(client);
	if client.login_status==HANDSHAKE_MESSAGE_PASSWORD_CHALLENGE:
		_receive_handshake(client);
	
	if client.login_status==HANDSHAKE_MESSAGE_SUCCESS:
		client._client_looper=threading.Thread(name="Client Looper",target=_connection_loop,args=(client,False));
		client._server_looper=threading.Thread(name="Server Looper",target=_connection_loop,args=(client,True));
		client.connected=True;
		client._client_looper.start();
		client._server_looper.start();
	else:
		pass;
	
def _send_handshake(client):
	"""
	Sends a handshake request to the server.
	"""
	#TODO Failure/password challenge handling
	select([client.conn_client],[],[]);
	login_string=b"";
	while login_string.count(b"\x00")<12:
		login_string+=client.conn_client.recv(1024);
	
	login_params=_unpack_login_string(login_string);
	func=client.on_login_handshake;
	login_params=func(client,login_params);
	login_string=_pack_login_string(login_params);
	
	client.conn_server.send(login_string);
	
def _receive_handshake(client):
	"""
	Receives and interprets a handshake response.
	"""
	select([client.conn_server],[],[]);
	response=b"";
	while len(response)<2 or response.count(b"\x00",1)==0:
		response+=client.conn_server.recv(1024);
	
	client.conn_client.send(response);
	client.login_status=response[0];
	client.login_response=response[1:len(response)-1];
	
	select([client.conn_client],[],[]);
	ack=b"";
	while b"\x00" not in ack:
		ack+=client.conn_client.recv(1024);
	client.conn_server.send(ack);
	
def _unpack_login_string(string):
	"""
	Creates a dictionary containing the parameters of the login string.
	"""
	login_fields=string.split(b"\x00");
	return {
			"playerName": login_fields[0],
			"password": login_fields[1],
			"screenDefinition": login_fields[2],
			"scaleNumerator": login_fields[3],
			"scaleDenominator": login_fields[4],
			"fontSize": login_fields[5],
			"systemArchitecture": login_fields[6],
			"javaEnvironment": login_fields[7],
			"unknown": login_fields[8],
			"hardwareAcceleration": login_fields[9],
			"graphicsMemory": login_fields[10],
			"signature": login_fields[11]
		};
	
def _pack_login_string(login_params):
	"""
	Creates a login string from the contents of the given dictionary.
	"""
	login_string=b"";
	login_string+=login_params["playerName"]+b"\x00";
	login_string+=login_params["password"]+b"\x00";
	login_string+=login_params["screenDefinition"]+b"\x00";
	login_string+=login_params["scaleNumerator"]+b"\x00";
	login_string+=login_params["scaleDenominator"]+b"\x00";
	login_string+=login_params["fontSize"]+b"\x00";
	login_string+=login_params["systemArchitecture"]+b"\x00";
	login_string+=login_params["javaEnvironment"]+b"\x00";
	login_string+=login_params["unknown"]+b"\x00";
	login_string+=login_params["hardwareAcceleration"]+b"\x00";
	login_string+=login_params["graphicsMemory"]+b"\x00";
	login_string+=login_params["signature"]+b"\x00";
	return login_string;
		
class Client:

	def __init__(self):
		self.local_port=21103;
		self.client_location="./AberothClient.jar";
		self.connected=False;
		self.login_status=HANDSHAKE_MESSAGE_NONE;
		self.login_response="";
		self.conn_client=None;
		self.conn_server=None;
		self.on_login_handshake=SIMPLE_FORWARD;
		self.on_data_to_client=SIMPLE_FORWARD;
		self.on_data_to_server=SIMPLE_FORWARD;
		self.on_message_to_client=SIMPLE_FORWARD;
		self.on_message_to_server=SIMPLE_FORWARD;
		self.on_command_to_client=SIMPLE_FORWARD;
		self.on_command_to_server=SIMPLE_FORWARD;
		
		self.launch_params={
				"playerName1": None,
				"password1": None,
				"showLogonDialog": None,
				"numClients": None,
				"delayBetweenClients": None,
				"mouseAdjustX": None,
				"mouseAdjustY": None,
				"fontSize": None,
				"scaleUp": None,
				"scaleDown": None,
				"screenDefinition": None,
				"isAppletSigned": None,
				"logCommandPercentages": None
			};
		
		self._client_process=None;
		self._conn_server_lock=threading.Lock();
		self._conn_client_lock=threading.Lock();
		self._client_thread=None;
		self._client_looper=None;
		self._server_looper=None;
		self._connection_thread=None;
			
	def start(self):
		"""
		Starts the client.
		"""
		def run_client():
			launcher_location=pkg_resources.resource_filename("incendium","launcher/ParamLauncher.jar");
			#args=shlex.split(self._get_launch_string('java',launcher_location,self.client_location));
			self._client_process=subprocess.Popen(self._get_launch_string('java',launcher_location,self.client_location));
			self._client_process.wait();
			pkg_resources.cleanup_resources();
		
		self._client_thread=threading.Thread(name="Aberoth Client",target=run_client);
		self._client_thread.start();
		
		self.reconnect();
	
	def reconnect(self):
		"""
		Reconnects client and server after the previous connection has been terminated.
		"""
		if not self.connected:
			self._connection_thread=threading.Thread(name="Connection Thread",target=_connect,args=(self,));
			self._connection_thread.start();
	
	def stop(self,makecamp=True):
		"""
		Closes the client.
		"""
		if makecamp:
			#TODO
			pass;
		self._client_process.terminate();
	
	def wait_for_connection(self,timeout=None):
		"""
		Blocks until a connection between the client and the server has been established.
		"""
		self._connection_thread.join(timeout=timeout);
		
	def send_to_server(self,message):
		"""
		Send a message directly to the server.
		"""
		stream=io.BytesIO();
		data.write_message(stream,message,warning=True);
		packet=_pack_message(stream.getvalue());
		with self._conn_server_lock:
			self.conn_server.send(packet);
	
	def send_to_client(self,message):
		"""
		Send a message directly to the client.
		"""
		stream=io.BytesIO();
		data.write_message(stream,message,warning=True);
		packet=_pack_message(stream.getvalue());
		with self._conn_client_lock:
			self.conn_client.send(packet);
		
	def _get_launch_string(self,java_location,launcher_location,client_location):
		launch='{0} "-Djava.ext.dirs={1}" -jar {2} {3}'.format(java_location,os.path.dirname(launcher_location),launcher_location,client_location);
		launch+=" serverIpAddress localhost ";
		launch+="serverPort "+str(self.local_port);
		for (k,v) in self.launch_params.items():
			if v:
				launch+=" "+k+" "+str(v);
		return launch;
