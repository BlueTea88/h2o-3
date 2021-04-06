package hex.schemas;

import hex.InfoGram.InfoGramModel;
import water.api.API;
import water.api.schemas3.ModelOutputSchemaV3;
import water.api.schemas3.ModelSchemaV3;


public class InfoGramModelV3 extends ModelSchemaV3<InfoGramModel, InfoGramModelV3, InfoGramModel.InfoGramParameters,
        InfoGramV3.InfoGramParametersV3, InfoGramModel.InfoGramModelOutput, InfoGramModelV3.InfoGramModelOutputV3> {
  public static final class InfoGramModelOutputV3 extends ModelOutputSchemaV3<InfoGramModel.InfoGramModelOutput, InfoGramModelOutputV3> {
    @API(help="Array of conditional mutual information for admissible features normalized to 0.0 and 1.0", 
            direction = API.Direction.OUTPUT)
    public double[] admissible_cmi;  // conditional mutual info for admissible features in _admissible_features

    @API(help="Array of conditional mutual information for admissible features raw and not normalized to 0.0 and 1.0",
            direction = API.Direction.OUTPUT)
    public double[] admissible_cmi_raw;  // raw conditional mutual info for admissible features in _admissible_features

    @API(help="Array of variable importance for admissible features", direction = API.Direction.OUTPUT)
    public double[] admissible_relevance;  // varimp values for admissible features in _admissible_features

    @API(help="Array containing names of admissible features for the user", direction = API.Direction.OUTPUT)
    public String[] admissible_features; // predictors chosen that exceeds both conditional_info and varimp thresholds

    @API(help="Array of raw conditional mutual information for all features excluding sensitive attributes if " +
            "applicable", direction = API.Direction.OUTPUT)
    public double[] cmi_raw; // cmi before normalization and for all predictors

    @API(help="Array of conditional mutual information for all features excluding sensitive attributes if applicable " +
            "normalized to 0.0 and 1.0", direction = API.Direction.OUTPUT)
    public double[] cmi;

    @API(help="Array containing names of all features excluding sensitive attributes if applicable corresponding to CMI" +
            " and relevance", direction = API.Direction.OUTPUT)
    public String[] all_predictor_names;

    @API(help="Array of variable importance for all features excluding sensitive attributes if applicable", 
            direction = API.Direction.OUTPUT)
    public double[] relevance; // variable importance for all predictors

    @API(help="frame key that stores the predictor names, net CMI and relevance", direction = API.Direction.OUTPUT)
    String relevance_cmi_key;
  }

  public InfoGramV3.InfoGramParametersV3 createParametersSchema() { return new InfoGramV3.InfoGramParametersV3(); }

  public InfoGramModelOutputV3 createOutputSchema() { return new InfoGramModelOutputV3(); }

  @Override
  public InfoGramModel createImpl() {
    InfoGramModel.InfoGramParameters parms = parameters.createImpl();
    return new InfoGramModel(model_id.key(), parms, null);
  }
}
