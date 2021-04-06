from __future__ import print_function
import os
import sys

from h2o.estimators.infogram import H2OInfoGramEstimator
from h2o.estimators.gbm import H2OGradientBoostingEstimator

sys.path.insert(1, os.path.join("..","..",".."))
import h2o
from tests import pyunit_utils
    
def test_infogram_iris_gbm_final_model():
    """
    Simple Iris test to check that we can set x = infogram model and final model = gbm yield the correct model.
    :return: 
    """
    fr = h2o.import_file(path=pyunit_utils.locate("smalldata/admissibleml_test/irisROriginal.csv"))
    target = "Species"
    fr[target] = fr[target].asfactor()
    x = fr.names
    x.remove(target)
    
    infogram_model = H2OInfoGramEstimator(seed = 12345, distribution = 'multinomial', model_algorithm='gbm') # build infogram model with default settings
    infogram_model.train(x=x, y=target, training_frame=fr)
    infogram_final_scoring_history = infogram_model._model_json["output"]["scoring_history"]
    final_gbm_model = H2OGradientBoostingEstimator(seed = 12345, distribution = 'multinomial')
    final_gbm_model.train(x=infogram_model, y=target, training_frame=fr)
    manual_scoring_history = final_gbm_model._model_json["output"]["scoring_history"]
    pyunit_utils.assert_H2OTwoDimTable_equal_upto(infogram_final_scoring_history, 
                                     manual_scoring_history,['number_of_trees', 'training_rmse', 'training_logloss',
                                                             'training_classification_error'])

if __name__ == "__main__":
    pyunit_utils.standalone_test(test_infogram_iris_gbm_final_model)
else:
    test_infogram_iris_gbm_final_model()
