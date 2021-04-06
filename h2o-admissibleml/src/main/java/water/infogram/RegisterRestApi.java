package water.infogram;

import hex.InfoGram.InfoGram;
import hex.InfoGram.InfoGramExtension;
import water.ExtensionManager;
import water.api.AlgoAbstractRegister;
import water.api.RestApiContext;
import water.api.SchemaServer;

public class RegisterRestApi extends AlgoAbstractRegister {
  @Override
  public void registerEndPoints(RestApiContext context) {
    InfoGramExtension ext = (InfoGramExtension) ExtensionManager.getInstance().getCoreExtension(InfoGramExtension.NAME);
    ext.logNativeLibInfo();
    InfoGram infogramMB = new InfoGram(true);
    // Register InfoGram model builder REST API
    registerModelBuilder(context, infogramMB, SchemaServer.getStableVersion());
  }

  @Override
  public String getName() {
    return "InfoGram";
  }
}
