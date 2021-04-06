package hex.InfoGram;

import hex.tree.xgboost.XGBoostExtension;
import org.apache.log4j.Logger;
import water.AbstractH2OExtension;

public class InfoGramExtension extends AbstractH2OExtension {
  private static final Logger LOG = Logger.getLogger(XGBoostExtension.class);
  public static String NAME = "InfoGram";
  @Override
  public String getExtensionName() {
    return NAME;
  }

  public void logNativeLibInfo() {
    LOG.info("InfoGramExtension is called.");
  }
}
