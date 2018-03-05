
import java.util.ListResourceBundle;

/**
Dummy bundle that returns the contents from the ParamLauncher.
*/
public class DummyBundle extends ListResourceBundle {
	
	private Object[][] contents;
	
	public DummyBundle(Object[][] contents){
		this.contents=contents;
	}

	@Override
	protected Object[][] getContents(){
		return contents;
	}
}