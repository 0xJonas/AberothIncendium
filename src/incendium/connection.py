import socket;
import threading;
import subprocess;
import zlib;
import pkg_resources;
import data;

def _connect(conn):
	server=socket.socket();
	server.bind(("localhost",conn._local_port));
	server.listen();
	conn.conn_client=server.accept()[0]; #TODO save address
	conn.conn_server=socket.socket();
	conn.conn_server.connect(("192.99.201.128",21103));
	
	conn._client_looper=threading.Thread(name="Client Looper",target=client_loop,args=(conn.conn_client,conn));
	conn._server_looper=threading.Thread(name="Server Looper",target=server_loop,args=(conn.conn_server,conn));
	conn._client_looper.start();
	conn._server_looper.start();
	conn.connected=True;
	
def server_loop(sock,conn):
	while True:
		message=_read_message(sock);
		with conn._transfer_to_client_lock:
			processed_messages=conn._transfer_to_client(message);
		for m in processed_messages:
			conn.send_to_client(m);

def client_loop(sock,conn):
	while True:
		message=_read_message(sock);
		with conn._transfer_to_server_lock:
			processed_messages=conn._transfer_to_server(message);
		for m in processed_messages:
			conn.send_to_server(m);
		
def _read_message(sock):
	size_data=sock.recv(3);
	size=0;
	if size_data[0]!=0xff:
		compressed=True;
		size=(size_data[0]<<16)+(size_data[1]<<8)+size_data[2];
	else:
		compressed=False;
		size=(size_data[1]<<8)+size_data[2];
	message=b"";
	bytes_received=0;
	while bytes_received<size:
		data=sock.recv(min(1024,size-bytes_received));
		message+=data;
		bytes_received+=len(data);
	if compressed:
		message=zlib.decompress(message);
	return message;

def simple_forward(msg):
	"""
	Transfer function that simply forwards the messages with no change.
	
	This is the default value for the client's transfer functions.
	"""
	return [msg];

class Connection:
	
	def __init__(self,client,local_port):
		self.client=client;
		self._local_port=local_port;
		self.connected=False;
		
		self._transfer_to_client=simple_forward;
		self._transfer_to_client_lock=threading.Lock();
		self._transfer_to_server=simple_forward;
		self._transfer_to_server_lock=threading.Lock();
		
	def _start_server(self):
		self.connection_thread=threading.Thread(name="Connection Thread",target=_connect,args=(self,));
		self.connection_thread.start();
		
	def wait_for_connection(self,timeout=-1):
		"""
		This function blocks until a connection between the client and the server has been established.
		"""
		self.connection_thread.join();
		
	def send_to_server(self,message,blocking=False):
		"""
		Sends a message to the server.
		"""
		#TODO
		pass;
		
	def send_to_client(self,message,blocking=False):
		"""
		Sends a message to the client.
		"""
		#TODO
		pass;
		
	def set_transfer_to_client(self,transfer_func):
		"""
		Sets the transfer function for messages to the client.
		"""
		with self._transfer_to_client_lock:
			self._transfer_to_client=transfer_func;
			
	def set_transfer_to_server(self,transfer_func):
		"""
		Sets the transfer function for messages to the server.
		"""
		with self._transfer_to_server_lock:
			self._transfer_to_server=transfer_func;
			
	def disconnect(self,makecamp=True):
		pass;

class Client:

	def __init__(self):
		self.local_port=21103;
		self.client_location="./AberothClient.jar";
		self.connected=False;
		
		self._launch_params={
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
		self._login_params={
				"playerName": "",
				"password": "",
				"screenDefinition": 1,
				"scaleNumerator": 1,
				"scaleDenominator": 1,
				"fontSize": 14,
				"systemArchitecture": "",
				"javaEnvironment": "",
				"unknown": True,
				"hardwareAcceleration": False,
				"graphicsMemory": 0,
				"signature": True
			};
	
	def start(self,local_port=21103):
		"""
		Starts the client.
		"""
		connection=Connection(self,local_port);
		connection._start_server();
		def run_client():
			launcher_location=pkg_resources.resource_filename("incendium","launcher/ParamLauncher.jar");
			subprocess.run(self._get_launch_string('java',launcher_location,self.client_location));
			pkg_resources.cleanup_resources();
		
		self._client_thread=threading.Thread(name="Aberoth Client",target=run_client);
		self._client_thread.start();
		return connection;
	
	def set_launch_params(self,playerName1=None,password1=None,showLogonDialog=None,numClients=None,delayBetweenClients=None,mouseAdjustX=None,mouseAdjustY=None,
							fontSize=None,scaleUp=None,scaleDown=None,screenDefinition=None,isAppletSigned=None,logCommandPercentages=None):
		"""
		Sets the launch parameters for the client via keyword arguments.
		"""
		if playerName1: self._launch_params["playerName1"]=playerName1;
		if password1: self._launch_params["password1"]=password1;
		if showLogonDialog: self._launch_params["showLogonDialog"]=showLogonDialog;
		if numClients: self._launch_params["numClients"]=numClients;
		if delayBetweenClients: self._launch_params["delayBetweenClients"]=delayBetweenClients;
		if mouseAdjustX: self._launch_params["mouseAdjustX"]=mouseAdjustX;
		if mouseAdjustY: self._launch_params["mouseAdjustY"]=mouseAdjustY;
		if fontSize: self._launch_params["fontSize"]=fontSize;
		if scaleUp: self._launch_params["scaleUp"]=scaleUp;
		if scaleDown: self._launch_params["scaleDown"]=scaleDown;
		if screenDefinition: self._launch_params["screenDefinition"]=screenDefinition;
		if isAppletSigned: self._launch_params["isAppletSigned"]=isAppletSigned;
		if logCommandPercentages: self._launch_params["logCommandPercentages"]=logCommandPercentages;
		
	def _get_launch_string(self,java_location,launcher_location,client_location):
		launch=java_location+' "-Djava.ext.dirs=." -cp .;'+client_location+' -jar '+launcher_location;
		launch+=" serverIpAddress localhost ";
		launch+="serverPort "+str(self.local_port);
		for (k,v) in self._launch_params.items():
			if v:
				launch+=" "+k+" "+str(v);
		return launch;
		
	def set_login_params(self,playerName=None,password=None,screenDefinition=None,scaleNumerator=None,scaleDenominator=None,fontSize=None,systemArchitecture=None,javaEnvironment=None,
						unknown=None,hardwareAcceleration=None,graphicsMemory=None,signature=None):
		"""
		Sets the login parameters for the client via keyword arguments.
		"""
		if playerName: self._login_params["playerName"]=playerName;
		if password: self._login_params["password"]=password;
		if screenDefinition: self._login_params["screenDefinition"]=screenDefinition;
		if scaleNumerator: self._launch_params["scaleNumerator"]=scaleNumerator;
		if scaleDenominator: self._launch_params["scaleDenominator"]=scaleDenominator;
		if fontSize: self._launch_params["fontSize"]=fontSize;
		if systemArchitecture: self._launch_params["systemArchitecture"]=systemArchitecture;
		if javaEnvironment: self._launch_params["javaEnvironment"]=javaEnvironment;
		if unknown: self._launch_params["unknown"]=unknown;
		if hardwareAcceleration: self._launch_params["hardwareAcceleration"]=hardwareAcceleration;
		if graphicsMemory: self._launch_params["graphicsMemory"]=graphicsMemory;
		if signature: self._launch_params["signature"]=signature;
		
	def _get_login_string(self):
		login = self._login_params["playerName"]+"\x00"
		+self._login_params["password"]+"\x00"
		+self._login_params["screenDefinition"]+"\x00"
		+self._login_params["scaleNumerator"]+"\x00"
		+self._login_params["scaleDenominator"]+"\x00"
		+self._login_params["fontSize"]+"\x00"
		+self._login_params["systemArchitecture"]+"\x00"
		+self._login_params["javaEnvironment"]+"\x00"
		+self._login_params["unknown"]+"\x00"
		+self._login_params["hardwareAcceleration"]+"\x00"
		+self._login_params["graphicsMemory"]+"\x00"
		+self._login_params["signature"]+"\x00"
		return login;
