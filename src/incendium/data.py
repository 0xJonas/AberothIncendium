import incendium.messages as msg;

def read_byte(stream):
	return stream.read(1)[0];

def write_byte(stream,value,warning=True):
	if value>255 and warning:
		print("Waring: Atempting to write byte larger than 255");
	b=value & 0xff;
	ba=bytearray(1);
	ba[0]=b;
	stream.write(ba);
	
def read_short(stream):
	msb=stream.read(1)[0];
	lsb=stream.read(1)[0];
	return (msb<<8)+lsb;
	
def write_short(stream,value,warning=True):
	if value>0xffff and warning:
		print("Warning: Atempting to write short larger than 65535");
	msb=(value>>8) & 0xff;
	lsb=value & 0xff;
	ba=bytearray(2);
	ba[0]=msb;
	ba[1]=lsb;
	stream.write(ba);
	
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
		ping_command=read_command(stream);
		return msg.FrameWithInfo(command_list,ping_command);
	elif message_id==msg.ONE_FRAME_NO_INFO_ID:
		length=read_byte(stream);
		length=(length<<8)+read_byte(stream);
		length=(length<<8)+read_byte(stream);
		command_list=[];
		for i in range(length):
			command_list.append(read_command(stream));
		return msg.FrameNoInfo(command_list);
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
		trigger=read_command(stream);
		data=b"";
		if trigger.echo_length>0 and trigger.echo_length<=3:
			data_length=1024<<(trigger.echo_length-1);
			data=stream.read(data_length);
		return msg.FrameReceived(trigger,data);
	elif message_id==msg.CLIENT_STATUS_ID:
		status=read_short(stream);
		return msg.ClientStatus(status);
	else:
		print("unknown message!");
		print(stream.read());

def write_message(stream,message,warning=True):
	write_byte(stream,message.get_id());
	if message.get_id()==msg.CREATE_WINDOW_ID:
		write_byte(stream,message.window_id,warning=warning);
		write_string(stream,message.title,warning=warning);
		write_short(stream,message.width,warning=warning);
		write_short(stream,message.height,warning=warning);
		#TODO
		write_byte(stream,2);
	elif message.get_id()==msg.ONE_FRAME_NO_INFO_ID:
		length=len(message.command_list);
		write_byte(stream,(length>>16) & 0xff,warning);
		write_byte(stream,(length>>8) & 0xff,warning);
		write_byte(stream,length & 0xff,warning);
		for command in message.command_list:
			write_command(stream,command,warning=warning);
	elif message.get_id()==msg.ONE_FRAME_WITH_INFO_ID:
		length=len(message.command_list);
		write_byte(stream,(length>>16) & 0xff,warning);
		write_byte(stream,(length>>8) & 0xff,warning);
		write_byte(stream,length & 0xff,warning);
		for command in message.command_list:
			write_command(stream,command,warning=warning);
		write_command(stream,message.ping_command,warning=warning);
	elif message.get_id()==msg.USER_INPUT_ID:
		#write_byte(stream,message.window_id,warning=warning);
		write_byte(stream,255,warning=warning);
		length=len(message.command_list);
		#length=2;
		write_byte(stream,(length>>16) & 0xff,warning);
		write_byte(stream,(length>>8) & 0xff,warning);
		write_byte(stream,length & 0xff,warning);
		for command in message.command_list:
			write_command(stream,command,warning=warning);
	elif message.get_id()==msg.CLIENT_STATUS_ID:
		write_short(stream,message.status,warning=warning);
	elif message.get_id()==msg.FRAME_RECEIVED_ID:
		write_command(stream,message.ping_command,warning=warning);
		stream.write(message.data);
	#TODO default

def read_command(stream):
	command_id=read_byte(stream);
	if command_id==msg.PING_ID_BANDWIDTH_CHECK_ID:
		unknown1=read_byte(stream);
		unknown2=read_byte(stream);
		echo_length=read_byte(stream);
		return msg.PingIdBandwidthCheck(unknown1,unknown2,echo_length);
	elif command_id==msg.DRAW_FILLED_RECT_AT_Y_PLUS_ONE_ID:
		return msg.FilledRectYPlusOne();
	elif command_id==msg.DRAW_FILLED_RECT_AT_X_PLUS_ONE_ID:
		return msg.FilledRectXPlusOne();
	elif command_id==msg.DRAW_FILLED_RECT_AT_DY_ID:
		delta=read_byte(stream);
		return msg.FilledRectDy(delta);
	elif command_id==msg.DRAW_FILLED_RECT_AT_DX_ID:
		delta=read_byte(stream);
		return msg.FilledRectDx(delta);
	elif command_id==msg.DRAW_FILLED_RECT_AT_BLOCK_XY_ID:
		x_pos=read_byte(stream);
		y_pos=read_byte(stream);
		return msg.FilledRectBlockXY(x_pos,y_pos);
	elif command_id==msg.DRAW_FILLED_RECT_AT_XY_ID:
		x_pos=read_short(stream);
		y_pos=read_short(stream);
		return msg.FilledRectXY(x_pos,y_pos);
	elif command_id==msg.DRAW_FILLED_RECT_AT_Y_PLUS_ONE_REPEAT_ID:
		rep_count=read_byte(stream);
		return msg.FilledRectYPlusOneRepeat(rep_count);
	elif command_id==msg.SET_FILLED_RECT_SIZE_ID:
		width=read_short(stream);
		height=read_short(stream);
		rounding=read_byte(stream);
		return msg.SetRectSize(width,height,(rounding & 1)!=0,(rounding & 2)!=0);
	elif command_id==msg.DRAW_PIXEL_ID:
		x_pos=read_short(stream);
		y_pos=read_short(stream);
		return msg.DrawPixel(x_pos,y_pos);
	elif command_id==msg.COPY_AREA_ID:
		source_x=read_short(stream);
		source_y=read_short(stream);
		width=read_short(stream);
		height=read_short(stream);
		destination_x=read_short(stream);
		destination_y=read_short(stream);
		if read_byte(stream)!=0:
			destination_x=-destination_x;
		if read_byte(stream)!=0:
			destination_y=-destination_y;
		return msg.CopyArea(source_x,source_y,width,height,destination_x,destination_y);
	elif command_id==msg.SET_COLOR_ID:
		r=read_byte(stream);
		g=read_byte(stream);
		b=read_byte(stream);
		return msg.SetColor(r,g,b);
	elif command_id==msg.SET_COLOR_WITH_ALPHA_ID:
		r=read_byte(stream);
		g=read_byte(stream);
		b=read_byte(stream);
		a=read_byte(stream);
		return msg.SetColorWithAlpha(r,g,b,a);
	elif command_id==msg.CACHE_CURRENT_COLOR_ID:
		cache_id=read_byte(stream);
		return msg.CacheColor(cache_id);
	elif command_id==msg.SET_COLOR_BASED_ON_CACHE_ID:
		cache_id=read_byte(stream);
		delta=read_byte(stream);
		return msg.SetColorBasedOnCache(cache_id,((delta>>5) & 7)-4,((delta>>2) & 7)-4,(delta & 3)-2);
	elif command_id==msg.SET_ON_SCREEN_TEXT_ID:
		text_id=read_short(stream);
		x_pos=read_short(stream);
		y_pos=read_short(stream);
		line_shift=read_byte(stream);
		style=read_byte(stream);
		font=read_byte(stream);
		content=read_string(stream);
		return msg.SetOnScreenText(text_id,x_pos,y_pos,line_shift,style,font,content);
	elif command_id==msg.MOVE_ON_SCREEN_TEXT_ID:
		text_id=read_short(stream);
		x_pos=read_short(stream);
		y_pos=read_short(stream);
		line_shift=read_byte(stream);
		return msg.MoveOnScreenText(text_id,x_pos,y_pos,line_shift);
	elif command_id==msg.SUB_WINDOW_ID:
		sub_command=read_byte(stream);
		subwindow_id=read_byte(stream);
		if sub_command==msg.CREATE_SUB_WINDOW_ID:
			x_pos=read_short(stream);
			y_pos=read_short(stream);
			width=read_short(stream);
			height=read_short(stream);
			return msg.CreateSubWindow(subwindow_id,x_pos,y_pos,width,height);
		elif sub_command==msg.SWITCH_TO_SUB_WINDOW_ID:
			return msg.SwitchToSubWindow(subwindow_id);
		elif sub_command==msg.SWITCH_BACK_TO_PREVIOUS_SUB_WINDOW_ID:
			return msg.SwitchToPreviousSubWindow(subwindow_id);
		elif sub_command==msg.DESTROY_SUB_WINDOW_ID:
			return msg.DestroySubWindow(subwindow_id);
	elif command_id==msg.USE_GLOBAL_RESOURCE_ID:
		resource_id=read_short(stream);
		sub_command=read_byte(stream);
		if sub_command==msg.RESOURCE_TYPE_IMAGE_NO_DATA_ID:
			x_pos=read_short(stream);
			y_pos=read_short(stream);
			return msg.ResourceImageNoData(resource_id,x_pos,y_pos);
		elif sub_command==msg.RESOURCE_TYPE_PNG_ID:
			x_pos=read_short(stream);
			y_pos=read_short(stream);
			length=read_short(stream);
			png_data=stream.read(length);
			return msg.ResourceImagePNG(resource_id,x_pos,y_pos,png_data);
		elif sub_command==msg.RESOURCE_TYPE_IMAGE_RAW_ID:
			x_pos=read_short(stream);
			y_pos=read_short(stream);
			length=read_short(stream);
			width=read_byte(stream);
			height=read_byte(stream);
			rgb_data=stream.read(length-2);
			return msg.ResourceImageRaw(resource_id,x_pos,y_pos,rgb_data);
		elif sub_command==msg.RESOURCE_TYPE_SOUND_EFFECT_NO_DATA_ID:
			pan=read_byte(stream);
			volume=read_byte(stream);
			instance_id=read_short(stream);
			return msg.ResourceSoundNoData(resource_id,instance_id,pan,volume);
		elif sub_command==msg.RESOURCE_TYPE_SOUND_EFFECT_ID:
			pan=read_byte(stream);
			volume=read_byte(stream);
			instance_id=read_short(stream);
			name=read_string(stream);
			return msg.ResourceSound(resource_id,instance_id,pan,volume,name);
		elif sub_command==msg.RESOURCE_TYPE_STOP_SOUND_EFFECT_ID:
			pan=read_byte(stream);
			volume=read_byte(stream);
			instance_id=read_short(stream);
			return msg.ResourceStopSound(resource_id,instance_id,pan,volume);
		elif sub_command==msg.RESOURCE_TYPE_MOVE_SOUND_EFFECT_ID:
			#TODO
			pass;
	elif command_id==msg.MOUSE_INPUT_ID:
		subwindow_id=read_byte(stream);
		button=read_byte(stream);
		action=read_byte(stream);
		x_pos=read_short(stream);
		y_pos=read_short(stream);
		return msg.MouseInput(subwindow_id,button,action,x_pos,y_pos);
	elif command_id==msg.KEYBOARD_INPUT_ID:
		key_code=read_byte(stream);
		action=read_byte(stream);
		return msg.KeyboardInput(key_code,action);
	elif command_id==msg.DATA_INPUT_ID:
		data=read_string();
		return msg.DataInput(data);
	else:
		return msg.LoadColor(command_id-30);
	
def write_command(stream,command,warning=True):
	command_id=command.get_id();
	write_byte(stream,command_id,warning);
	if command_id==msg.PING_ID_BANDWIDTH_CHECK_ID:
		write_byte(stream,command.unknown1,warning);
		write_byte(stream,command.unknown2,warning);
		write_byte(stream,command.echo_length,warning);
	elif command_id==msg.DRAW_FILLED_RECT_AT_Y_PLUS_ONE_ID:
		pass;
	elif command_id==msg.DRAW_FILLED_RECT_AT_X_PLUS_ONE_ID:
		pass;
	elif command_id==msg.DRAW_FILLED_RECT_AT_DY_ID:
		write_byte(stream,command.delta,warning);
	elif command_id==msg.DRAW_FILLED_RECT_AT_DX_ID:
		write_byte(stream,command.delta,warning);
	elif command_id==msg.DRAW_FILLED_RECT_AT_BLOCK_XY_ID:
		write_byte(stream,command.x_pos,warning);
		write_byte(stream,command.y_pos,warning);
	elif command_id==msg.DRAW_FILLED_RECT_AT_XY_ID:
		write_short(stream,command.x_pos,warning);
		write_short(stream,command.y_pos,warning);
	elif command_id==msg.DRAW_FILLED_RECT_AT_Y_PLUS_ONE_REPEAT_ID:
		write_byte(stream,command.rep_count,warning);
	elif command_id==msg.SET_FILLED_RECT_SIZE_ID:
		write_short(stream,command.width,warning);
		write_short(stream,command.height,warning);
		rounding=0;
		if command.round_up_x:
			rounding+=1;
		if command.round_up_y:
			rounding+=2;
		write_byte(stream,rounding,warning);
	elif command_id==msg.DRAW_PIXEL_ID:
		write_short(stream,command.x_pos,warning);
		write_short(stream,command.y_pos,warning);
	elif command_id==msg.COPY_AREA_ID:
		write_short(stream,command.source_x,warning);
		write_short(stream,command.source_y,warning);
		write_short(stream,command.width,warning);
		write_short(stream,command.height,warning);
		write_short(stream,abs(command.destination_x),warning);
		write_short(stream,abs(command.destination_y),warning);
		write_byte(stream,0 if command.destination_x>=0 else 1,warning);
		write_byte(stream,0 if command.destination_y>=0 else 1,warning);
	elif command_id==msg.SET_COLOR_ID:
		write_byte(stream,command.red,warning);
		write_byte(stream,command.green,warning);
		write_byte(stream,command.blue,warning);
	elif command_id==msg.SET_COLOR_WITH_ALPHA_ID:
		write_byte(stream,command.red,warning);
		write_byte(stream,command.green,warning);
		write_byte(stream,command.blue,warning);
		write_byte(stream,command.alpha,warning);
	elif command_id==msg.CACHE_CURRENT_COLOR_ID:
		write_byte(stream,command.index,warning);
	elif command_id==msg.SET_COLOR_BASED_ON_CACHE_ID:
		write_byte(stream,command.index,warning);
		color_delta=(command.blue_delta+2) & 3;
		color_delta|=((command.green_delta+4) & 7)<<2;
		color_delta|=((command.red_delta+4) & 7)<<5;
		write_byte(stream,color_delta,warning);
	elif command_id==msg.SET_ON_SCREEN_TEXT_ID:
		write_short(stream,command.text_id,warning);
		write_short(stream,command.x_pos,warning);
		write_short(stream,command.y_pos,warning);
		write_byte(stream,command.line_shift,warning);
		write_byte(stream,command.style,warning);
		write_byte(stream,command.font,warning);
		write_string(stream,command.content,warning);
	elif command_id==msg.MOVE_ON_SCREEN_TEXT_ID:
		write_short(stream,command.text_id,warning);
		write_short(stream,command.x_pos,warning);
		write_short(stream,command.y_pos,warning);
		write_byte(stream,command.line_shift,warning);
	elif command_id==msg.SUB_WINDOW_ID:
		sub_command=command.sub_command;
		write_byte(stream,sub_command,warning);
		write_byte(stream,command.subwindow_id,warning);
		if sub_command==msg.CREATE_SUB_WINDOW_ID:
			write_short(stream,command.x_pos,warning);
			write_short(stream,command.y_pos,warning);
			write_short(stream,command.width,warning);
			write_short(stream,command.height,warning);
		elif sub_command==msg.SWITCH_TO_SUB_WINDOW_ID:
			pass;
		elif sub_command==msg.SWITCH_BACK_TO_PREVIOUS_SUB_WINDOW_ID:
			pass;
		elif sub_command==msg.DESTROY_SUB_WINDOW_ID:
			pass;
	elif command_id==msg.USE_GLOBAL_RESOURCE_ID:
		sub_command=command.sub_command;
		write_short(stream,command.resource_id,warning);
		write_byte(stream,sub_command,warning);
		if sub_command==msg.RESOURCE_TYPE_IMAGE_NO_DATA_ID:
			write_short(stream,command.x_pos,warning);
			write_short(stream,command.y_pos,warning);
		if sub_command==msg.RESOURCE_TYPE_PNG_ID:
			write_short(stream,command.x_pos,warning);
			write_short(stream,command.y_pos,warning);
			write_short(stream,len(command.png_data),warning);
			stream.write(command.png_data);
		if sub_command==msg.RESOURCE_TYPE_IMAGE_RAW_ID:
			write_short(stream,command.x_pos,warning);
			write_short(stream,command.y_pos,warning);
			write_short(stream,len(command.rgb_data)-2,warning);
			write_byte(stream,command.width,warning);
			write_byte(stream,command.height,warning);
			stream.write(command.rgb_data);
		if sub_command==msg.RESOURCE_TYPE_SOUND_EFFECT_NO_DATA_ID:
			write_byte(stream,command.pan,warning);
			write_byte(stream,command.volume,warning);
			write_short(stream,command.instance_id,warning);
		if sub_command==msg.RESOURCE_TYPE_SOUND_EFFECT_ID:
			write_byte(stream,command.pan,warning);
			write_byte(stream,command.volume,warning);
			write_short(stream,command.instance_id,warning);
			write_string(stream,command.name,warning);
		if sub_command==msg.RESOURCE_TYPE_STOP_SOUND_EFFECT_ID:
			write_byte(stream,command.pan,warning);
			write_byte(stream,command.volume,warning);
			write_short(stream,command.instance_id,warning);
		if sub_command==msg.RESOURCE_TYPE_MOVE_SOUND_EFFECT_ID:
			#TODO
			pass;
	elif command_id==msg.MOUSE_INPUT_ID:
		write_byte(stream,command.subwindow_id,warning);
		write_byte(stream,command.button,warning);
		write_byte(stream,command.action,warning);
		write_short(stream,command.x_pos,warning);
		write_short(stream,command.y_pos,warning);
	elif command_id==msg.KEYBOARD_INPUT_ID:
		write_byte(stream,command.key_code,warning);
		write_byte(stream,command.action,warning);
	elif command_id==msg.DATA_INPUT_ID:
		write_string(stream,command.data);
	else:
		pass;
