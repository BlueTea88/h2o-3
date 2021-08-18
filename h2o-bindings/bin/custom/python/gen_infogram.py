rest_api_version = 3  # type: int

def update_param(name, param):
    if name == 'infogram_algorithm_params':
        param['type'] = 'KeyValue'
        param['default_value'] = None
        return param
    return None  # param untouched


def class_extensions():
    def get_relevance_cmi_frame(self):
        """
        Get the relevance and CMI for all attributes returned by InfoGram as an H2O Frame.
        :param self: 
        :return: H2OFrame
        """
        keyString = self._model_json["output"]["relevance_cmi_key"]
        if not (keyString == None):
            return h2o.get_frame(keyString)
        else:
            return None

    def get_admissible_attributes(self):
        """
        Get the admissible attributes
        :param self: 
        :return: 
        """
        if not (self._model_json["output"]["admissible_features"] == None):
            return self._model_json["output"]["admissible_features"]
        else:
            return None

    def get_admissible_relevance(self):
        """
        Get the relevance of admissible attributes
        :param self: 
        :return: 
        """
        if not (self._model_json["output"]["admissible_relevance"] == None):
            return self._model_json["output"]["admissible_relevance"]
        else:
            return None

    def get_admissible_cmi(self):
        """
        Get the normalized cmi of admissible attributes
        :param self: 
        :return: 
        """
        if not (self._model_json["output"]["admissible_cmi"] == None):
            return self._model_json["output"]["admissible_cmi"]
        else:
            return None

    def get_admissible_cmi_raw(self):
        """
        Get the raw cmi of admissible attributes
        :param self: 
        :return: 
        """
        if not (self._model_json["output"]["admissible_cmi_raw"] == None):
            return self._model_json["output"]["admissible_cmi_raw"]
        else:
            return None

    def get_all_predictor_relevance(self):
        """
        Get relevance of all predictors
        :param self: 
        :return: two tuples, first one is predictor names and second one is relevance
        """
        if not (self._model_json["output"]["all_predictor_names"] == None):
            return self._model_json["output"]["all_predictor_names"], self._model_json["output"]["relevance"]
        else:
            return None


    def get_all_predictor_cmi(self):
        """
        Get normalized cmi of all predictors.
        :param self: 
        :return: two tuples, first one is predictor names and second one is cmi
        """
        if not (self._model_json["output"]["all_predictor_names"] == None):
            return self._model_json["output"]["all_predictor_names"], self._model_json["output"]["cmi"]
        else:
            return None


    def get_all_predictor_cmi_raw(self):
        """
        Get raw cmi of all predictors.
        :param self: 
        :return: two tuples, first one is predictor names and second one is cmi
        """
        if not (self._model_json["output"]["all_predictor_names"] == None):
            return self._model_json["output"]["all_predictor_names"], self._model_json["output"]["cmi_raw"]
        else:
            return None
        
    # Override train method to support infogram needs
    def train(self, x=None, y=None, training_frame=None, blending_frame=None, verbose=False, **kwargs):
        sup = super(self.__class__, self)
        
        def extend_parms(parms): # add parameter checks specific to infogram
            training_col_names = training_frame.names
            if not(parms["conditional_info_threshold"] == None):
                assert_is_type(parms["conditional_info_threshold"], numeric)
                assert parms["conditional_info_threshold"] >= 0 and parms["conditional_info_threshold"] <= 1,\
                    "conditional_info_threshold should be between 0 and 1."
            if not(parms["varimp_threshold"] == None):
                assert_is_type(parms["varimp_threshold"], numeric)
                assert parms["varimp_threshold"] >= 0 and parms["varimp_threshold"] <= 1, "varimp_threshold should be" \
                                                                                      " between 0 and 1."
            if not(parms["data_fraction"] == None):
                assert_is_type(parms["data_fraction"], numeric)
                assert parms["data_fraction"] > 0 and parms["data_fraction"] <= 1, "data_fraction should exceed 0" \
                                                                               " and <= 1."
        
        parms = sup._make_parms(x,y,training_frame, extend_parms_fn = extend_parms, **kwargs)
        sup._train(parms, verbose=verbose)
        # can probably get rid of model attributes that Erin does not want here
        return self

extensions = dict(
    __imports__="""
import ast
import json
import h2o
from h2o.utils.typechecks import assert_is_type, is_type, numeric
from h2o.frame import H2OFrame
from h2o.exceptions import H2OValueError
""",
    __class__=class_extensions
)
       
overrides = dict(
    infogram_algorithm_params=dict(
        getter="""
if self._parms.get("{sname}") != None:
    infogram_algorithm_params_dict =  ast.literal_eval(self._parms.get("{sname}"))
    for k in infogram_algorithm_params_dict:
        if len(infogram_algorithm_params_dict[k]) == 1: #single parameter
            infogram_algorithm_params_dict[k] = infogram_algorithm_params_dict[k][0]
    return infogram_algorithm_params_dict
else:
    return self._parms.get("{sname}")
""",
        setter="""
assert_is_type({pname}, None, {ptype})
if {pname} is not None and {pname} != "":
    for k in {pname}:
        if ("[" and "]") not in str(infogram_algorithm_params[k]):
            infogram_algorithm_params[k] = [infogram_algorithm_params[k]]
    self._parms["{sname}"] = str(json.dumps({pname}))
else:
    self._parms["{sname}"] = None
"""
    )
)

doc = dict(
    __class__="""
Given a sensitive/unfair predictors list, InfoGram will add all predictors that contains information on the 
 sensitive/unfair predictors list to the sensitive/unfair predictors list.  It will return a set of predictors that
 do not contain information on the sensitive/unfair list and hence user can build a fair model.  If no sensitive/unfair
 predictor list is given, InfoGram will return a list of core predictors that should be used to build a final model.
 InfoGram can significantly cut down the number of predictors needed to build a model and hence will build a simple
 model that is more interpretable, less susceptible to overfitting, runs faster while providing similar accuracy
 as models built using all attributes.
"""
)
