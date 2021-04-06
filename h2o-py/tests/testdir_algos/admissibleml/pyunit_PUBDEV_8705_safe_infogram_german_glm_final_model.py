from __future__ import print_function
import os
import sys

from h2o.estimators.infogram import H2OInfoGramEstimator
from h2o.estimators.glm import H2OGeneralizedLinearEstimator

sys.path.insert(1, os.path.join("..","..",".."))
import h2o
from tests import pyunit_utils
    
def test_infogram_german_data_glm_final_model():
    """
    Simple German data to check that a glm final model can be built either inside the infogram itself or 
    by call drf and specify x = infogram_model.
    :return: 
    """
    fr = h2o.import_file(path=pyunit_utils.locate("smalldata/admissibleml_test/german_credit.csv"))
    target = "BAD"
    fr[target] = fr[target].asfactor()
    x = fr.names
    x.remove(target)
    x.remove("status_gender")
    x.remove( "age")
    infogram_model = H2OInfoGramEstimator(seed = 12345, sensitive_attributes=["status_gender", "age"], ntop=50, 
                                          model_algorithm='glm', distribution='bernoulli')
    infogram_model.train(x=x, y=target, training_frame=fr)
    infogram_final_scoring_history = infogram_model._model_json["output"]["scoring_history"]

    manual_model_glm = H2OGeneralizedLinearEstimator(seed=12345)
    manual_model_glm.train(x=infogram_model, y=target, training_frame=fr)
    manual_scoring_history = manual_model_glm._model_json["output"]["scoring_history"]
    # make sure final model in infogram is the same as manually built one.
    pyunit_utils.assert_H2OTwoDimTable_equal_upto(infogram_final_scoring_history,
                                              manual_scoring_history,['negative_log_likelihood', 'objective'])




if __name__ == "__main__":
    pyunit_utils.standalone_test(test_infogram_german_data_glm_final_model)
else:
    test_infogram_german_data_glm_final_model()
