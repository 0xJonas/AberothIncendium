
CREATE_WINDOW_ID=0x14;
ONE_FRAME_NO_INFO_ID=0x0c;
ONE_FRAME_WITH_INFO_ID=0x17;
USER_INPUT_ID=0x0e;
FRAME_RECEIVED_ID=0x0d;
CLIENT_STATUS_ID=0x16;

PING_ID_BANDWIDTH_CHECK_ID=0x0b;
DRAW_FILLED_RECT_AT_Y_PLUS_ONE_ID=0x00;
DRAW_FILLED_RECT_AT_X_PLUS_ONE_ID=0x03;
DRAW_FILLED_RECT_AT_DY_ID=0x02;
DRAW_FILLED_RECT_AT_DX_ID=0x04;
DRAW_FILLED_RECT_AT_BLOCK_XY_ID=0x01;
DRAW_FILLED_RECT_AT_XY_ID=0x05;
DRAW_FILLED_RECT_AT_Y_PLUS_ONE_REPEAT_ID=0x1b;
SET_FILLED_RECT_SIZE_ID=0x19;
DRAW_PIXEL_ID=0x12;
COPY_AREA_ID=0x15;
SET_COLOR_ID=0x06;
SET_COLOR_WITH_ALPHA_ID=0x1d;
CACHE_CURRENT_COLOR_ID=0x07;
SET_COLOR_BASED_ON_CACHE_ID=0x1c;
SET_ON_SCREEN_TEXT_ID=0x08;
MOVE_ON_SCREEN_TEXT_ID=0x09;
SUB_WINDOW_ID=0x18;
CREATE_SUB_WINDOW_ID=0x00;
SWITCH_TO_SUB_WINDOW_ID=0x01;
SWITCH_BACK_TO_PREVIOUS_SUB_WINDOW_ID=0x02;
DESTROY_SUB_WINDOW_ID=0x03;
USE_GLOBAL_RESOURE_ID=0x1a;
RESOURCE_TYPE_IMAGE_NO_DATA_ID=0x00;
RESOURCE_TYPE_IMAGE_PNG_ID=0x01;
RESOURCE_TYPE_IMAGE_RAW_ID=0x05;
RESOURCE_TYPE_SOUND_EFFECT_NO_DATA_ID=0x02;
RESOURCE_TYPE_SOUND_EFFECT_ID=0x03;
RESOURCE_TYPE_MOVE_SOUND_EFFECT_ID=0x04;
RESOURCE_TYPE_STOP_SOUND_EFFECT_ID=0x06;
MOUSE_INPUT_ID=0x13;
KEYBOARD_INPUT_ID=0x10;

class Command:
	
	def get_id(self):
		pass;
		
	def get_length(self):
		pass
	
class Message:

	def __init__(self,time=-1):
		self.time=time;
		
	def get_id(self):
		pass;
		
	def get_length(self):
		pass
		
#==================================
#=============Messages=============
#==================================
		
class CreateWindow(Message):

	def __init__(self,windowId,title,width,height,key_events,mouse_events,mouse_motion_events,time=-1):
		super().__init__(time=time);
		self.windowId=windowId;
		self.title=title;
		self.width=width;
		self.height=height;
		self.key_events=key_events;
		self.mouse_events=mouse_events;
		self.mouse_motion_events=mouse_motion_events;
	
	def get_id(self):
		return CREATE_WINDOW_MESSAGE;
	
	def get_length(self):
		return len(self.title)+9; #string length + string content + 7
		
class FrameNoInfo(Message):
	
	def __init__(self,command_list,time=-1):
		super().__init__(time=time);
		self.command_list=command_list;
	
	def get_id(self):
		return ONE_FRAME_NO_INFO_ID;
		
	def get_length(self):
		length=4; #id + command_list length
		for c in self.command_list:
			length+=c.get_length();
		return length;
		
class FrameWithInfo(Message):
	
	def __init__(self,command_list,ping_command,time=-1):
		super().__init__(time=time);
		self.command_list=command_list;
		self.ping_command=ping_command;
		
	def get_id(self):
		return ONE_FRAME_WITH_INFO_ID;
		
	def get_length(self):
		length=4; #id + command_list length
		length+=self.ping_command.get_length();
		for c in self.command_list:
			length+=c.get_length();
		return length;

class UserInput(Message):
	
	def __init__(self,windowId,input_commands,time=-1):
		super().__init__(time=time);
		self.windowId=windowId;
		self.input_commands=self.input_commands;
		
	def get_id(self):
		return USER_INPUT_ID;
		
	def get_length(self):
		length=6;
		for c in self.input_commands:
			length+=c.get_length();
		return length;
		
class FrameReceived(Message):
	
	def __init__(self,ping_command,data=None,time=-1):
		super().__init__(time=time);
		self.ping_command=ping_command;
		self.data=data;
		
	def get_id(self):
		return FRAME_RECEIVED_ID;
		
	def get_length(self):
		#TODO handle data==None
		return 1+self.ping_command.get_length()+len(data);
		
class ClientStatus(Message):
	
	def __init__(self,status,time=-1):
		super().__init__(time=time),
		self.status=status;
		
	def get_id():
		return CLIENT_STATUS_ID;
		
	def get_length(self):
		return 3;
		
#==================================
#=============Commands=============
#==================================

class PingIdBandwidthCheck(Command):
	
	def __init__(self,unknown1,unknown2,echo_length,time=-1):
		super().__init__(time=time);
		self.unknown1=unknown1;
		self.unknown2=unknown2;
		self.echo_length=echo_length;
		
	def get_id(self):
		return PING_ID_BANDWIDTH_CHECK_ID;
		
	def get_length(self):
		return 4;
		
	def __str__(self):
		return "PING_ID_BANDWIDTH_CHECK echo={0}, unknown1={1}, unknown2={2}".format(self.echo_length,self.unknown1,self.unknown2);
		
class FilledRectYPlusOne(Command):
	
	def __init__(self,time=-1):
		super().__init__(time=time);
		
	def get_id(self):
		return DRAW_FILLED_RECT_AT_Y_PLUS_ONE_ID;
		
	def get_length(self):
		return 1;
	
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_Y_PLUS_ONE";
		
class FilledRectXPlusOne(Command):
	
	def __init__(self,time=-1):
		super().__init__(time=time);
		
	def get_id(self):
		return DRAW_FILLED_RECT_AT_X_PLUS_ONE;
		
	def get_length(self):
		return 1;
	
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_X_PLUS";
		
class FilledRectDy(Command):
	
	def __init__(self,delta,time=-1):
		super().__init__(time=time);
		self.delta=delta;
		
	def get_id(self):
		return DRAW_FILLED_RECT_AT_DY_ID;
		
	def get_length(self):
		return 2;
	
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_DY delta="+self.delta;
		
class FilledRectDx(Command):
	
	def __init__(self,delta,time=-1):
		super().__init__(time=time);
		self.delta=delta;
		
	def get_id(self):
		return DRAW_FILLED_RECT_AT_DX_ID;
		
	def get_length(self):
		return 2;
	
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_DX delta="+self.delta;
		
class FilledRectBlockXY(Command):
	
	def __init__(self,x_pos,y_pos,time=-1):
		super().__init__(time=time);
		self.x_pos=x_pos;
		self.y_pos=y_pos;
	
	def get_id(self):
		return DRAW_FILLED_RECT_AT_BLOCK_XY_ID;
	
	def get_length(self):
		return 3;
	
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_BLOCK_XY ({0},{1})".format(self.x_pos,self.y_pos);
		
class FilledRectXY(Command):
	
	def __init__(self,x_pos,y_pos,time=-1):
		super().__init__(time=time);
		self.x_pos=x_pos;
		self.y_pos=y_pos;
	
	def get_id(self):
		return DRAW_FILLED_RECT_AT_XY_ID;
	
	def get_length(self):
		return 3;
	
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_XY ({0},{1})".format(self.x_pos,self.y_pos);
		
class FilledRectYPlusOneRepeat(Command):
	
	def __init__(self,rep_count,time=-1):
		super().__init__(time=time);
		self.rep_count=rep_count;
		
	def get_id(self):
		return DRAW_FILLED_RECT_AT_Y_PLUS_ONE_REPEAT_ID;
		
	def get_length(self):
		return 2;
		
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_Y_PLUS_ONE_REPEAT "+self.rep_count;
		
class SetRectSize(Command):
	
	def __init__(self,width,height,round_up_x,round_up_y,time=-1):
		super().__init__(time=time);
		self.width=width;
		self.height=height;
		self.round_up_x=round_up_x;
		self.round_up_y=round_up_y;
		
	def get_id(self):
		return SET_FILLED_RECT_SIZE_ID;
		
	def get_length(self):
		return 6;
	
	def __str__(self):
		return "SET_FILLED_RECT_SIZE {0}x{1} round x {2}, round y {3}".format(self.width,self.height,"up" if self.round_up_x else "down","up" if self.round_up_y else "down");

class DrawPixel(Command):
	
	def __init__(self,x_pos,y_pos,time=-1):
		super().__init__(time=time);
		self.x_pos=x_pos;
		self.y_pos=y_pos;
	
	def get_id(self):
		return DRAW_PIXEL_ID;
		
	def get_length(self):
		return 5;
		
	def __str__(self):
		return "DRAW_PIXEL ({0},{1})".format(self.x_pos,self.y_pos);
		
class CopyArea(Command):
	
	def __init__(self,source_x,source_y,width,height,destination_x,destination_y,time=-1):
		super().__init__(time=time);
		self.source_x=source_x;
		self.source_y=source_y;
		self.width=width;
		self.height=height;
		self.destination_x=destination_x;
		self.destination_y=destination_y;
		
	def get_id(self):
		return COPY_AREA_ID;
		
	def get_length(self):
		return 15;
	
	def __str__(self):
		return "COPY_AREA Source=({0},{1}) Destination=({2},{3}) Area={4}x{5}".format(self.source_x,self.source_y,self.destination_x,self.destination_y,self.width,self.height);

class SetColor(Command):
	
	def __init__(self,red,green,blue,time=-1):
		super().__init__(time=time);
		self.red=red;
		self.green=green;
		self.blue=blue;
	
	def get_id(self):
		return SET_COLOR_ID;
	
	def get_length(self):
		return 4;
	
	def get_rgba(self):
		return (self.red<<24)+(self.green<<16)+(self.blue<<8)+0xff;
	
	def __str__(self):
		return "SET_COLOR rgba: #{0:X}".format(self.get_rgba());
		
class SetColorWithAlpha(Command):
	
	def __init__(self,red,green,blue,alpha,time=-1):
		super().__init__(time=time);
		self.red=red;
		self.green=green;
		self.blue=blue;
		self.alpha=alpha;

	def get_id(self):
		return SET_COLOR_WITH_ALPHA_ID;
	
	def get_length(self):
		return 5;
	
	def get_rgba(self):
		return (self.red<<24)+(self.green<<16)+(self.blue<<8)+self.alpha;
	
	def __str__(self):
		return "SET_COLOR_WITH_ALPHA rgba: #{0:X}".format(self.get_rgba());
		
class CacheColor(Command):
	
	def __init__(self,index,time=-1):
		super().__init__(time=time);
		self.index=index;
	
	def get_id(self):
		return CACHE_CURRENT_COLOR_ID;
	
	def get_length(self):
		return 2;
	
	def __str__(self):
		return "CACHE_CURRENT_COLOR "+self.index;
		
class SetColorBasedOnCache(Command):
	
	def __init__(self,index,red_delta,green_delta,blue_delta,time=-1):
		super().__init__(time=time);
		self.index=index;
		self.red_delta=red_delta;
		self.green_delta=green_delta;
		self.blue_delta=blue_delta;
		
	def get_id(self):
		return SET_COLOR_BASED_ON_CACHE_ID;
	
	def get_length(self):
		return 3;
	
	def __str__(self):
		return "SET_COLOR_BASED_ON_CACHE red{0}{1} green{2}{3} blue{4}{5}".format("+" if self.red_delta>=0 else "",self.red_delta,"+" if self.green_delta>=0 else "",self.green_delta,"+" if self.blue_delta>=0 else "",self.blue_delta);
