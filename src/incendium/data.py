import messages as msg;

def read_byte(stream):
	return stream.read(1)[0];

def write_byte(stream,value,warning=True):
	if value>255 and warning:
		print("Waring: Atempting to write byte larger than 255");
	b=value & 0xff;
	stream.write(b""+b);
	
def read_short(stream):
	msb=stream.read(1)[0];
	lsb=stream.read(1)[0];
	return (msb<<8)+lsb;
	
def write_short(stream,value,warning=True):
	if value>0xffff and warning:
		print("Warning: Atempting to write short larger than 65535");
	msb=(value>>8) & 0xff;
	lsb=value & 0xff;
	stream.write(msb+b""+lsb);
	
def write_string(stream,value,warning=True):
	if len(value)>0xffff and warning:
		print("Warning: Atempting to write string longer than 65535 characters");
	write_short(stream,len(value));
	stream.write(bytes(value,"utf-8"));
	
def read_string(stream):
	length=read_short(stream);
	content=stream.read(length);
	return str(content,"utf-8");
	
def read_message(stream):
	message_id=read_byte(stream);
	if message_id==msg.CREATE_WINDOW_ID:
		window_id=read_byte(stream);
		title=read_string(stream);
		width=read_short(stream);
		height=read_short(stream);
		events=read_byte(stream);
		
		key_events=events!=1;
		mouse_events=events!=0;
		mouse_motion_events=events in [1,3];
		
		return msg.CreateWindow(window_id,title,width,height,key_events,mouse_events,mouse_motion_events);
	elif message_id==msg.ONE_FRAME_WITH_INFO_ID:
		length=read_byte(stream);
		length=(length<<8)+read_byte(stream);
		length=(length<<8)+read_byte(stream);
		command_list=[];
		for i in range(length):
			command_list.append(read_command(stream));
		return msg.FrameNoInfo(command_list);
	elif message_id==msg.ONE_FRAME_NO_INFO_ID:
		length=read_byte(stream);
		length=(length<<8)+read_byte(stream);
		length=(length<<8)+read_byte(stream);
		command_list=[];
		for i in range(length):
			command_list.append(read_command(stream));
		ping_command=read_command(stream);
		return msg.FrameNoInfo(command_list,ping_command);
	elif message_id==msg.USER_INPUT_ID:
		window_id=read_byte(stream);
		length=read_byte(stream);
		length=(length<<8)+read_byte(stream);
		length=(length<<8)+read_byte(stream);
		command_list=[];
		for i in range(length):
			command_list.append(read_command(stream));
		return msg.UserInput(window_id,command_list);
	elif message_id==msg.FRAME_RECEIVED_ID:
		#TODO
		pass;
	elif message_id==msg.CLIENT_STATUS_ID:
		status=read_short(stream);
		return msg.ClientStatus(status);
	#Todo default

def write_message(stream,message,warning=True):
	if message.get_id()==msg.CREATE_WINDOW_ID:
		write_byte(stream,msg.CREATE_WINDOW_ID,warning=warning);
		write_string(stream,message.title,warning=warning);
		write_short(stream,message.width,warning=warning);
		write_short(stream,message.height,warning=warning);
		
	elif message.get_id()==msg.ONE_FRAME_NO_INFO_ID:
		pass;
	elif message.get_id()==msg.ONE_FRAME_WITH_INFO_ID:
		pass;
	elif message.get_id()==msg.USER_INPUT_ID:
		pass;
	elif message.get_id()==msg.CLIENT_STATUS_ID:
		write_byte(stream,msg.CLIENT_STATUS_ID);
		write_short(stream,message.status,warning=warning);
	#TODO default

def read_command(stream):
	command_id=read_byte(stream);
	if command_id==msg.PING_ID_BANDWIDTH_CHECK_ID:
		pass;
	elif command_id==msg.DRAW_FILLED_RECT_AT_Y_PLUS_ONE_ID:
		pass;
	elif command_id==msg.DRAW_FILLED_RECT_AT_X_PLUS_ONE_ID:
		pass;
	elif command_id==msg.DRAW_FILLED_RECT_AT_DY_ID:
		pass;
	elif command_id==msg.DRAW_FILLED_RECT_AT_DX_ID:
		pass;
	elif command_id==msg.DRAW_FILLED_RECT_AT_BLOCK_XY_ID:
		pass;
	elif command_id==msg.DRAW_FILLED_RECT_AT_XY_ID:
		pass;
	elif command_id==msg.DRAW_FILLED_RECT_AT_Y_PLUS_ONE_REPEAT_ID:
		pass;
	elif command_id==msg.SET_FILLED_RECT_SIZE_ID:
		pass;
	elif command_id==msg.DRAW_PIXEL_ID:
		pass;
	elif command_id==msg.COPY_AREA_ID:
		pass;
	elif command_id==msg.SET_COLOR_ID:
		pass;
	elif command_id==msg.SET_COLOR_WITH_ALPHA_ID:
		pass;
	elif command_id==msg.CACHE_CURRENT_COLOR_ID:
		pass;
	elif command_id==msg.SET_COLOR_BASED_ON_CACHE_ID:
		pass;
	elif command_id==msg.SET_ON_SCREEN_TEXT_ID:
		pass;
	elif command_id==msg.MOVE_ON_SCREEN_TEXT_ID:
		pass;
	elif command_id==msg.SUB_WINDOW_ID:
		pass;
	elif command_id==msg.USE_GLOBAL_RESOURCE_ID:
		pass;
	elif command_id==msg.MOUSE_INPUT_ID:
		pass;
	elif command_id==msg.KEYBOARD_INPUT_ID:
		pass;
	else:
		pass;
	
def write_command(stream,command,warning=True):
	if command.get_id()==msg.PING_ID_BANDWIDTH_CHECK_ID:
		pass;
	elif command.get_id()==msg.DRAW_FILLED_RECT_AT_Y_PLUS_ONE_ID:
		pass;
	elif command.get_id()==msg.DRAW_FILLED_RECT_AT_X_PLUS_ONE_ID:
		pass;
	elif command.get_id()==msg.DRAW_FILLED_RECT_AT_DY_ID:
		pass;
	elif command.get_id()==msg.DRAW_FILLED_RECT_AT_DX_ID:
		pass;
	elif command.get_id()==msg.DRAW_FILLED_RECT_AT_BLOCK_XY_ID:
		pass;
	elif command.get_id()==msg.DRAW_FILLED_RECT_AT_XY_ID:
		pass;
	elif command.get_id()==msg.DRAW_FILLED_RECT_AT_Y_PLUS_ONE_REPEAT_ID:
		pass;
	elif command.get_id()==msg.SET_FILLED_RECT_SIZE_ID:
		pass;
	elif command.get_id()==msg.DRAW_PIXEL_ID:
		pass;
	elif command.get_id()==msg.COPY_AREA_ID:
		pass;
	elif command.get_id()==msg.SET_COLOR_ID:
		pass;
	elif command.get_id()==msg.SET_COLOR_WITH_ALPHA_ID:
		pass;
	elif command.get_id()==msg.CACHE_CURRENT_COLOR_ID:
		pass;
	elif command.get_id()==msg.SET_COLOR_BASED_ON_CACHE_ID:
		pass;
	elif command.get_id()==msg.SET_ON_SCREEN_TEXT_ID:
		pass;
	elif command.get_id()==msg.MOVE_ON_SCREEN_TEXT_ID:
		pass;
	elif command.get_id()==msg.SUB_WINDOW_ID:
		pass;
	elif command.get_id()==msg.USE_GLOBAL_RESOURCE_ID:
		pass;
	elif command.get_id()==msg.MOUSE_INPUT_ID:
		pass;
	elif command.get_id()==msg.KEYBOARD_INPUT_ID:
		pass;
	else:
		pass;
