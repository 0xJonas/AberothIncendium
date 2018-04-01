
import java.io.File;
import java.net.URLClassLoader;
import java.net.URL;

/**
IMPORTANT:
The jarfile has to be executed with the command 'java "-Djava.ext.dirs=ParamLauncher.jar" -jar ParamLauncher.jar AberothClient.jar <args>'
*/
public class ParamLauncher {
	
	public static Object[][] dummyResource={
		{"serverIpAddress","192.99.201.128"},
		{"serverPort","21103"},
		{"playerName1",""},
		{"password1",""},
		{"showLogonDialog","true"},
		{"numClients","1"},
		{"delayBetweenClients","0"},
		{"mouseAdjustX","0"},
		{"mouseAdjustY","0"},
		{"fontSize","14"},
		{"scaleUp","1"},
		{"scaleDown","1"},
		{"screenDefinition","-1"},
		{"isAppletSigned","true"},
		{"playbackFromFile","false"},
		{"playbackFileName","None.abr"},
		{"logCommandPercentages","false"}
		};
		
	public static Object[][] getDummyResources(){
		return dummyResource;
	}
		
	private static int indexOf(String str){
		for(int i=0;i<dummyResource.length;i++){
			if(str.equals(dummyResource[i][0]))
				return i;
		}
		return -1;
	}
	
	public static void main(String[] args){
		String clientLocation=args[0];
		for(int i=1;i<args.length;i+=2){
			String key=args[i];
			String value=args[i+1];
			int index=indexOf(key);
			if(index!=-1){
				dummyResource[index][1]=value;
			}
		}
		try{
			URLClassLoader ucl=new URLClassLoader(new URL[]{new File(clientLocation).toURI().toURL()});
			Class<?> client=ucl.loadClass("gameclient.GameClient");
			client.getMethod("main",String[].class).invoke(null,(Object) new String[0]);
		}catch(Exception e){
			e.printStackTrace();
		}
	}
}