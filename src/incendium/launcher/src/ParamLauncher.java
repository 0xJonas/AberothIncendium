
import java.util.ListResourceBundle;
import java.util.jar.JarFile;
import java.util.jar.JarEntry;
import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;
import java.io.InputStream;
import java.io.IOException;

/**
IMPORTANT:
The jarfile has to be executed with the command 'java "-Djava.ext.dirs=." -jar ParamLauncher.jar <args>'
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
		for(int i=0;i<args.length;i+=2){
			String key=args[i];
			String value=args[i+1];
			int index=indexOf(key);
			if(index!=-1){
				dummyResource[index][1]=value;
			}
		}
		gameclient.GameClient.main(new String[0]);
	}
}