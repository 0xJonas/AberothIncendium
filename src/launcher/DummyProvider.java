
import java.util.spi.ResourceBundleControlProvider;
import java.util.ResourceBundle;
import java.util.Locale;
import java.io.IOException;

/**
Dummy service provider so that the getBundle("gameclient/GameClient") call in the Aberoth client receives our custom bundle instead of nothing.
*/
public class DummyProvider implements ResourceBundleControlProvider {
	
	private final String GAMECLIENT_BUNDLE_BASE_NAME="gameclient/GameClient";
	
	public DummyProvider(){
		
	}
	
	@Override
	public ResourceBundle.Control getControl(String baseName){
		if(baseName.equals(GAMECLIENT_BUNDLE_BASE_NAME))
			return new ResourceBundle.Control(){
				
				@Override
				public ResourceBundle newBundle(String baseName,Locale locale,String format,ClassLoader loader, boolean reload) 
						throws IllegalAccessException,InstantiationException,IOException{
					
					//Return the DummyBundle if the Aberoth clients call is recognized, otherwise use default behaviour
					if(baseName.startsWith(GAMECLIENT_BUNDLE_BASE_NAME))
						return new DummyBundle(ParamLauncher.getDummyResources());
					else
						return super.newBundle(baseName,locale,format,loader,reload);
				}
			};
		else 
			return null;
	}
}