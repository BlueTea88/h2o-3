from __future__ import print_function
import os
import sys

from h2o.estimators.infogram import H2OInfoGramEstimator
from h2o.estimators.random_forest import H2ORandomForestEstimator

sys.path.insert(1, os.path.join("..","..",".."))
import h2o
from tests import pyunit_utils
    
def test_infogram_personal_loan_drf_final_model():
    """
    Simple Perosnal loan test to check that a drf final model can be built either inside the infogram itself or 
    by call drf and specify x = infogram_model.
    :return: 
    """
    fr = h2o.import_file(path=pyunit_utils.locate("smalldata/admissibleml_test/Bank_Personal_Loan_Modelling.csv"))
    target = "Personal Loan"
    fr[target] = fr[target].asfactor()
    x = ["Experience","Income","Family","CCAvg","Education","Mortgage",
         "Securities Account","CD Account","Online","CreditCard"]
    infogram_model = H2OInfoGramEstimator(seed = 12345, sensitive_attributes=["Age","ZIP Code"], model_algorithm='drf')
    infogram_model.train(x=x, y=target, training_frame=fr)
    infogram_final_scoring_history = infogram_model._model_json["output"]["scoring_history"]
    
    manual_model_drf = H2ORandomForestEstimator(seed=12345)
    manual_model_drf.train(x=infogram_model, y=target, training_frame=fr)
    manual_scoring_history = manual_model_drf._model_json["output"]["scoring_history"]
    # make sure final model in infogram is the same as manually built one.
    pyunit_utils.assert_H2OTwoDimTable_equal_upto(infogram_final_scoring_history,
                                                  manual_scoring_history,['number_of_trees', 'training_rmse', 'training_logloss',
                                                                          'training_classification_error'])
        
if __name__ == "__main__":
    pyunit_utils.standalone_test(test_infogram_personal_loan_drf_final_model)
else:
    test_infogram_personal_loan_drf_final_model()
