
CREATE_WINDOW_ID=0x14;
ONE_FRAME_NO_INFO_ID=0x17;
ONE_FRAME_WITH_INFO_ID=0x0c;
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
USE_GLOBAL_RESOURCE_ID=0x1a;
RESOURCE_TYPE_IMAGE_NO_DATA_ID=0x00;
RESOURCE_TYPE_PNG_ID=0x01;
RESOURCE_TYPE_IMAGE_RAW_ID=0x05;
RESOURCE_TYPE_SOUND_EFFECT_NO_DATA_ID=0x02;
RESOURCE_TYPE_SOUND_EFFECT_ID=0x03;
RESOURCE_TYPE_MOVE_SOUND_EFFECT_ID=0x04;
RESOURCE_TYPE_STOP_SOUND_EFFECT_ID=0x06;
MOUSE_INPUT_ID=0x13;
KEYBOARD_INPUT_ID=0x10;
DATA_INPUT_ID=0x11;

#TODO add more keys
key_codes={
	"cancel": 3,
	"backspace": 8,
	"tab": 9,
	"enter": 10,
	"clear": 12,
	"shift": 16,
	"control": 17,
	"alt": 18,
	"capslock": 20,
	"escape": 27,
	"convert": 28,
	"space": 32,
	"home": 36,
	"left": 37,
	"up": 38,
	"right": 39,
	"down": 40,
	
};
for i in range(44,58):
	key_codes[chr(i)]=i;
for i in range(65,91):	#a - z
	key_codes[chr(i+32)]=i;
for i in range(112,124): #F1 - F12
	key_codes["f"+chr(i-111)]=i;

class Command:

	def __init__(self,time=-1):
		#TODO not required since same as message?
		self.time=time;
	
	def get_id(self):
		pass;
	
class Message:

	def __init__(self,time=-1):
		self.time=time;
		
	def get_id(self):
		pass;
		
#==================================
#=============Messages=============
#==================================
		
class CreateWindow(Message):

	def __init__(self,window_id,title,width,height,key_events,mouse_events,mouse_motion_events,time=-1):
		super().__init__(time=time);
		self.window_id=window_id;
		self.title=title;
		self.width=width;
		self.height=height;
		self.key_events=key_events;
		self.mouse_events=mouse_events;
		self.mouse_motion_events=mouse_motion_events;
	
	def get_id(self):
		return CREATE_WINDOW_ID;
	
	def __len__(self):
		return len(self.title)+9; #string length + string content + 7
		
	def __str__(self):
		return "CREATE_WINDOW {0} id {1} size {2}x{3}".format(self.title,self.window_id,self.width,self.height);
		
class FrameNoInfo(Message):
	
	def __init__(self,command_list,time=-1):
		super().__init__(time=time);
		self.command_list=command_list;
	
	def get_id(self):
		return ONE_FRAME_NO_INFO_ID;
		
	def __len__(self):
		length=4; #id + command_list length
		for c in self.command_list:
			length+=c.get_length();
		return length;
		
	def __str__(self):
		return "ONE_FRAME_NO_INFO"; #TODO
		
class FrameWithInfo(Message):
	
	def __init__(self,command_list,ping_command,time=-1):
		super().__init__(time=time);
		self.command_list=command_list;
		self.ping_command=ping_command;
		
	def get_id(self):
		return ONE_FRAME_WITH_INFO_ID;
		
	def __len__(self):
		length=4; #id + command_list length
		length+=self.ping_command.get_length();
		for c in self.command_list:
			length+=c.get_length();
		return length;
	
	def __str__(self):
		return "ONE_FRAME_WITH_INFO"; #TODO

class UserInput(Message):
	
	def __init__(self,window_id,command_list,time=-1):
		super().__init__(time=time);
		self.window_id=window_id;
		self.command_list=command_list;
		
	def get_id(self):
		return USER_INPUT_ID;
		
	def __len__(self):
		length=6;
		for c in self.command_list:
			length+=c.get_length();
		return length;
		
	def __str__(self):
		return "USER_INPUT"; #TODO
		
class FrameReceived(Message):
	
	def __init__(self,ping_command,data=None,time=-1):
		super().__init__(time=time);
		self.ping_command=ping_command;
		self.data=data;
		
	def get_id(self):
		return FRAME_RECEIVED_ID;
		
	def __len__(self):
		#TODO handle data==None
		return 1+self.ping_command.get_length()+len(data);
		
	def __str__(self):
		return "FRAME_RECEIVED"; #TODO
		
class ClientStatus(Message):
	
	def __init__(self,status,time=-1):
		super().__init__(time=time),
		self.status=status;
		
	def get_id(self):
		return CLIENT_STATUS_ID;
		
	def __len__(self):
		return 3;
	
	def __str__(self):
		return "CLIENT_STATUS"; #TODO
		
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
		
	def __len__(self):
		return 4;
		
	def __str__(self):
		return "PING_ID_BANDWIDTH_CHECK echo={0}, unknown1={1}, unknown2={2}".format(self.echo_length,self.unknown1,self.unknown2);
		
class FilledRectYPlusOne(Command):
	
	def __init__(self,time=-1):
		super().__init__(time=time);
		
	def get_id(self):
		return DRAW_FILLED_RECT_AT_Y_PLUS_ONE_ID;
		
	def __len__(self):
		return 1;
	
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_Y_PLUS_ONE";
		
class FilledRectXPlusOne(Command):
	
	def __init__(self,time=-1):
		super().__init__(time=time);
		
	def get_id(self):
		return DRAW_FILLED_RECT_AT_X_PLUS_ONE_ID;
		
	def __len__(self):
		return 1;
	
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_X_PLUS";
		
class FilledRectDy(Command):
	
	def __init__(self,delta,time=-1):
		super().__init__(time=time);
		self.delta=delta;
		
	def get_id(self):
		return DRAW_FILLED_RECT_AT_DY_ID;
		
	def __len__(self):
		return 2;
	
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_DY delta="+str(self.delta);
		
class FilledRectDx(Command):
	
	def __init__(self,delta,time=-1):
		super().__init__(time=time);
		self.delta=delta;
		
	def get_id(self):
		return DRAW_FILLED_RECT_AT_DX_ID;
		
	def __len__(self):
		return 2;
	
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_DX delta="+str(self.delta);
		
class FilledRectBlockXY(Command):
	
	def __init__(self,x_pos,y_pos,time=-1):
		super().__init__(time=time);
		self.x_pos=x_pos;
		self.y_pos=y_pos;
	
	def get_id(self):
		return DRAW_FILLED_RECT_AT_BLOCK_XY_ID;
	
	def __len__(self):
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
	
	def __len__(self):
		return 3;
	
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_XY ({0},{1})".format(self.x_pos,self.y_pos);
		
class FilledRectYPlusOneRepeat(Command):
	
	def __init__(self,rep_count,time=-1):
		super().__init__(time=time);
		self.rep_count=rep_count;
		
	def get_id(self):
		return DRAW_FILLED_RECT_AT_Y_PLUS_ONE_REPEAT_ID;
		
	def __len__(self):
		return 2;
		
	def __str__(self):
		return "DRAW_FILLED_RECT_AT_Y_PLUS_ONE_REPEAT "+str(self.rep_count);
		
class SetRectSize(Command):
	
	def __init__(self,width,height,round_up_x,round_up_y,time=-1):
		super().__init__(time=time);
		self.width=width;
		self.height=height;
		self.round_up_x=round_up_x;
		self.round_up_y=round_up_y;
		
	def get_id(self):
		return SET_FILLED_RECT_SIZE_ID;
		
	def __len__(self):
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
		
	def __len__(self):
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
		
	def __len__(self):
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
	
	def __len__(self):
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
	
	def __len__(self):
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
	
	def __len__(self):
		return 2;
	
	def __str__(self):
		return "CACHE_CURRENT_COLOR "+str(self.index);
		
class SetColorBasedOnCache(Command):
	
	def __init__(self,index,red_delta,green_delta,blue_delta,time=-1):
		super().__init__(time=time);
		self.index=index;
		self.red_delta=red_delta;
		self.green_delta=green_delta;
		self.blue_delta=blue_delta;
		
	def get_id(self):
		return SET_COLOR_BASED_ON_CACHE_ID;
	
	def __len__(self):
		return 3;
	
	def __str__(self):
		return "SET_COLOR_BASED_ON_CACHE red{0}{1} green{2}{3} blue{4}{5}".format("+" if self.red_delta>=0 else "",self.red_delta,"+" if self.green_delta>=0 else "",self.green_delta,"+" if self.blue_delta>=0 else "",self.blue_delta);

class SetOnScreenText(Command):

	STYLE_PLAIN=0;
	STYLE_ITALICS=1;
	STYLE_BOLD=2;
	STYLE_SMALL=3;
	
	TEXT_ID_CLEAR=0;
	TEXT_ID_STATS=2;
	TEXT_ID_HINT=3;
	TEXT_ID_BROADCAST=4;
	TEXT_ID_STATUS=65001;
	TEXT_ID_Y_LOCK=65535;
	
	def __init__(self,text_id,x_pos,y_pos,line_shift,style,font,content,time=-1):
		super().__init__(time=time);
		self.text_id=text_id;
		self.x_pos=x_pos;
		self.y_pos=y_pos;
		self.line_shift=line_shift;
		self.style=style;
		self.font=font;
		self.content=content;
		
	def get_id(self):
		return SET_ON_SCREEN_TEXT_ID;
	
	def __len__(self):
		return 10+2+len(self.content);
		
	def __str__(self):
		return "SET_ON_SCREEN_TEXT id {0}, ({1},{2}) : {3}".format(self.text_id,self.x_pos,self.y_pos,self.content);

class MoveOnScreenText(Command):
	
	def __init__(self,text_id,x_pos,y_pos,line_shift,time=-1):
		super().__init__(time=time);
		self.text_id=text_id;
		self.x_pos=x_pos;
		self.y_pos=y_pos;
		self.line_shift=line_shift;
	
	def get_id(self):
		return MOVE_ON_SCREEN_TEXT_ID;
	
	def __len__(self):
		return 8;
	
	def __str__(self):
		return "MOVE_ON_SCREEN_TEXT id {0}, ({1},{2})".format(self.text_id,self.x_pos,self.y_pos);
	
class SubWindowCommand(Command):
	
	def __init__(self,sub_command,subwindow_id,time=-1):
		super().__init__(time=time);
		self.sub_command=sub_command;
		self.subwindow_id=subwindow_id;
	
	def get_id(self):
		return SUB_WINDOW_ID;
	
	def __len__(self):
		return None;

class CreateSubWindow(SubWindowCommand):
	
	def __init__(self,subwindow_id,x_pos,y_pos,width,height,time=-1):
		super().__init__(CREATE_SUB_WINDOW_ID,subwindow_id,time=time);
		self.x_pos=x_pos;
		self.y_pos=y_pos;
		self.width=width;
		self.height=height;
	
	def __len__(self):
		return 11;
	
	def __str__(self):
		return "CREATE_SUB_WINDOW id {0}, at ({1},{2}) dimensions {3}x{4}".format(self.subwindow_id,self.x_pos,self.y_pos,self.width,self.height);
		
class SwitchToSubWindow(SubWindowCommand):
	
	def __init__(self,subwindow_id,time=-1):
		super().__init__(SWITCH_TO_SUB_WINDOW_ID,subwindow_id,time=time);
	
	def __len__(self):
		return 3;
	
	def __str__(self):
		return "SWITCH_TO_SUB_WINDOW id "+str(self.subwindow_id);
		
class SwitchToPreviousSubWindow(SubWindowCommand):
	
	def __init__(self,subwindow_id=0,time=-1):
		super().__init__(SWITCH_BACK_TO_PREVIOUS_SUB_WINDOW_ID,subwindow_id,time=time);
	
	def __len__(self):
		return 3;
	
	def __str__(self):
		return "SWITCH_BACK_TO_PREVIOUS_SUB_WINDOW";

class DestroySubWindow(SubWindowCommand):
	
	def __init__(self,subwindow_id,time=-1):
		super().__init__(DESTROY_SUB_WINDOW_ID,subwindow_id,time=time);
	
	def __len__(self):
		return 3;
	
	def __str__(self):
		return "DESTROY_SUB_WINDOW id "+str(self.subwindow_id);
		
class UseGlobalResource(Command):
	
	def __init__(self,sub_command,resource_id,time=-1):
		super().__init__(time=time);
		self.sub_command=sub_command;
		self.resource_id=resource_id;
		
	def get_id(self):
		return USE_GLOBAL_RESOURCE_ID;

	def __len__(self):
		return None;
	
class ResourceImageNoData(UseGlobalResource):
	
	def __init__(self,resource_id,x_pos,y_pos,time=-1):
		super().__init__(RESOURCE_TYPE_IMAGE_NO_DATA_ID,resource_id,time=time);
		self.x_pos=x_pos;
		self.y_pos=y_pos;
	
	def __len__(self):
		return 8;
	
	def __str__(self):
		return "RESOURCE_TYPE_IMAGE_NO_DATA id {0}, at ({1},{2})".format(self.resource_id,self.x_pos,self.y_pos);
	
class ResourceImagePNG(UseGlobalResource):
	
	def __init__(self,resource_id,x_pos,y_pos,png_data,time=-1):
		super().__init__(RESOURCE_TYPE_PNG_ID,resource_id,time=time);
		self.x_pos=x_pos;
		self.y_pos=y_pos;
		self.png_data=png_data;
		
	def __len__(self):
		return 10+len(png_data);
	
	def __str__(self):
		return "RESOURCE_TYPE_PNG id {0}, at ({1},{2})".format(self.resource_id,self.x_pos,self.y_pos);
		
class ResourceImageRaw(UseGlobalResource):

	def __init__(self,resource_id,x_pos,y_pos,width,height,rgb_data,time=-1):
		super().__init__(RESOURCE_TYPE_PNG_ID,resource_id,time=time);
		self.x_pos=x_pos;
		self.y_pos=y_pos;
		self.width=width;
		self.height=height;
		self.rgb_data=rgb_data;
		
	def __len__(self):
		return 12+len(rgb_data);
	
	def __str__(self):
		return "RESOURCE_TYPE_IMAGE_RAW id {0}, at ({1},{2})".format(self.resource_id,self.x_pos,self.y_pos);

class ResourceSoundNoData(UseGlobalResource):
	
	def __init__(self,resource_id,instance_id,pan,volume,time=-1):
		super().__init__(RESOURCE_TYPE_SOUND_EFFECT_NO_DATA_ID,resource_id,time=time);
		self.pan=pan;
		self.volume=volume;
		self.instance_id=instance_id;
	
	def __len__(self):
		return 8;
	
	def get_pan(self,client="Java"):
		if self.pan>127:
			p=-(~self.pan & 0xff)-1;
		else:
			p=self.pan;
		if client.lower()=="java":
			
			return self.pan/127*0.8;
		elif client.lower()=="html5":
			return self.pan/127;
	
	def get_volume(self):
		if self.volume>127:
			v=-(~self.volume & 0xff)-1;
		else:
			v=self.volume;
		return 10.0**(v/10.0);
	
	def __str__(self):
		return "RESOURCE_TYPE_SOUND_EFFECT_NO_DATA {0} volume {1:%}, {2:%} {3}".format(self.instance_id,self.volume,abs(self.pan),"left" if self.pan<0 else "right");
		
class ResourceSound(UseGlobalResource):
	
	def __init__(self,resource_id,instance_id,pan,volume,name,time=-1):
		super().__init__(RESOURCE_TYPE_SOUND_EFFECT_ID,resource_id,time=time);
		self.pan=pan;
		self.volume=volume;
		self.instance_id=instance_id;
		self.name=name;
	
	def __len__(self):
		return 10+len(name);
	
	def get_pan(self,client="Java"):
		if self.pan>127:
			p=-(~self.pan & 0xff)-1;
		else:
			p=self.pan;
		if client.lower()=="java":
			
			return self.pan/127*0.8;
		elif client.lower()=="html5":
			return self.pan/127;
	
	def get_volume(self):
		if self.volume>127:
			v=-(~self.volume & 0xff)-1;
		else:
			v=self.volume;
		return 10.0**(v/10.0);
			
	def __str__(self):
		return "RESOURCE_TYPE_SOUND_EFFECT {0} {1} volume {2:%}, {3:%} {4}".format(self.name,self.instance_id,self.volume,abs(self.pan),"left" if self.pan<0 else "right");
		
class ResourceStopSound(UseGlobalResource):
	
	def __init__(self,resource_id,instance_id,pan=0.0,volume=1.0,time=-1):
		super().__init__(RESOURCE_TYPE_STOP_SOUND_EFFECT_ID,resource_id,time=time);
		self.pan=pan;
		self.volume=volume;
		self.instance_id=instance_id;
	
	def __len__(self):
		return 8;
		
	def get_pan(self,client="Java"):
		if self.pan>127:
			p=-(~self.pan & 0xff)-1;
		else:
			p=self.pan;
		if client.lower()=="java":
			
			return self.pan/127*0.8;
		elif client.lower()=="html5":
			return self.pan/127;
	
	def get_volume(self):
		if self.volume>127:
			v=-(~self.volume & 0xff)-1;
		else:
			v=self.volume;
		return 10.0**(v/10.0);
	
	def __str__(self):
		return "RESOURCE_TYPE_STOP_SOUND_EFFECT "+str(self.instance_id);
		
class MouseInput(Command):

	MOUSE_PRESSED=0;
	MOUSE_RELEASED=1;
	MOUSE_MOVED=2;
	MOUSE_DRAGGED=3;
	
	def __init__(self,subwindow_id,button,action,x_pos,y_pos,time=-1):
		super().__init__(time=time);
		self.subwindow_id=subwindow_id;
		self.button=button;
		self.action=action;
		self.x_pos=x_pos;
		self.y_pos=y_pos;
	
	def get_id(self):
		return MOUSE_INPUT_ID;
		
	def __len__(self):
		return 8;
	
	def __str__(self):#TODO fix
		return "MOUSE_INPUT {0} at ({1},{2}) with button {3}".format(("pressed","released","moved","dragged")[self.action],self.x_pos,self.y_pos,self.button);

class KeyboardInput(Command):
	
	KEY_PRESSED=0;
	KEY_RELEASED=1;
	KEY_TYPED=2;
	KEY_SPECIAL=11;
	KEY_SPEECH=12;
	
	SPECIAL_START_ATTACK=1;
	SPECIAL_STOP_ATTACK=2;
	SPECIAL_START_DROP=3;
	SPECIAL_STOP_DROP=4;
	SPECIAL_START_SPEECH=5;
	SPECIAL_FINISH_SPEECH=6;
	
	def __init__(self,key_code,action,time=-1):
		super().__init__(time=time);
		self.key_code=key_code;
		self.action=action;
	
	def get_id(self):
		return KEYBOARD_INPUT_ID;
	
	def __len__(self):
		return 3;
	
	def __str__(self):
		return "KEYBOARD_INPUT action {0}, key {1}".format(self.action,self.key_code);
		
class DataInput(Command):
	
	def __init__(self,data,time=-1):
		self.data=data;
	
	def get_id(self):
		return KEYBOARD_INPUT_ID;
		
	def __len__(self):
		return 3+len(data);
	
	def __str__(self):
		return "DATA_INPUT "+self.data;
		
class LoadColor(Command):
	
	def __init__(self,index,time=-1):
		super().__init__(time=time);
		self.index=index;
	
	def get_id(self):
		return self.index+30;
	
	def __len__(self):
		return 1;
	
	def __str__(self):
		return "LOAD_COLOR_FROM_CACHE "+str(self.index);