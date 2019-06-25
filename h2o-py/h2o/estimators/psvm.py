#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This file is auto-generated by h2o-3/h2o-bindings/bin/gen_python.py
# Copyright 2016 H2O.ai;  Apache License Version 2.0 (see LICENSE for details)
#
from __future__ import absolute_import, division, print_function, unicode_literals

from h2o.estimators.estimator_base import H2OEstimator
from h2o.exceptions import H2OValueError
from h2o.frame import H2OFrame
from h2o.utils.typechecks import assert_is_type, Enum, numeric


class H2OSupportVectorMachineEstimator(H2OEstimator):
    """
    PSVM

    """

    algo = "psvm"

    def __init__(self, **kwargs):
        super(H2OSupportVectorMachineEstimator, self).__init__()
        self._parms = {}
        names_list = {"model_id", "training_frame", "validation_frame", "response_column", "ignored_columns",
                      "ignore_const_cols", "hyper_param", "kernel_type", "gamma", "rank_ratio", "positive_weight",
                      "negative_weight", "disable_training_metrics", "sv_threshold", "fact_threshold",
                      "feasible_threshold", "surrogate_gap_threshold", "mu_factor", "max_iterations", "seed"}
        if "Lambda" in kwargs: kwargs["lambda_"] = kwargs.pop("Lambda")
        for pname, pvalue in kwargs.items():
            if pname == 'model_id':
                self._id = pvalue
                self._parms["model_id"] = pvalue
            elif pname in names_list:
                # Using setattr(...) will invoke type-checking of the arguments
                setattr(self, pname, pvalue)
            else:
                raise H2OValueError("Unknown parameter %s = %r" % (pname, pvalue))

    @property
    def training_frame(self):
        """
        Id of the training data frame.

        Type: ``H2OFrame``.
        """
        return self._parms.get("training_frame")

    @training_frame.setter
    def training_frame(self, training_frame):
        self._parms["training_frame"] = H2OFrame._validate(training_frame, 'training_frame')


    @property
    def validation_frame(self):
        """
        Id of the validation data frame.

        Type: ``H2OFrame``.
        """
        return self._parms.get("validation_frame")

    @validation_frame.setter
    def validation_frame(self, validation_frame):
        self._parms["validation_frame"] = H2OFrame._validate(validation_frame, 'validation_frame')


    @property
    def response_column(self):
        """
        Response variable column.

        Type: ``str``.
        """
        return self._parms.get("response_column")

    @response_column.setter
    def response_column(self, response_column):
        assert_is_type(response_column, None, str)
        self._parms["response_column"] = response_column


    @property
    def ignored_columns(self):
        """
        Names of columns to ignore for training.

        Type: ``List[str]``.
        """
        return self._parms.get("ignored_columns")

    @ignored_columns.setter
    def ignored_columns(self, ignored_columns):
        assert_is_type(ignored_columns, None, [str])
        self._parms["ignored_columns"] = ignored_columns


    @property
    def ignore_const_cols(self):
        """
        Ignore constant columns.

        Type: ``bool``  (default: ``True``).
        """
        return self._parms.get("ignore_const_cols")

    @ignore_const_cols.setter
    def ignore_const_cols(self, ignore_const_cols):
        assert_is_type(ignore_const_cols, None, bool)
        self._parms["ignore_const_cols"] = ignore_const_cols


    @property
    def hyper_param(self):
        """
        Penalty parameter C of the error term

        Type: ``float``  (default: ``1``).
        """
        return self._parms.get("hyper_param")

    @hyper_param.setter
    def hyper_param(self, hyper_param):
        assert_is_type(hyper_param, None, numeric)
        self._parms["hyper_param"] = hyper_param


    @property
    def kernel_type(self):
        """
        Type of used kernel

        One of: ``"gaussian"``  (default: ``"gaussian"``).
        """
        return self._parms.get("kernel_type")

    @kernel_type.setter
    def kernel_type(self, kernel_type):
        assert_is_type(kernel_type, None, Enum("gaussian"))
        self._parms["kernel_type"] = kernel_type


    @property
    def gamma(self):
        """
        Coefficient of the kernel (currently RBF gamma for gaussian kernel, -1 means 1/#features)

        Type: ``float``  (default: ``-1``).
        """
        return self._parms.get("gamma")

    @gamma.setter
    def gamma(self, gamma):
        assert_is_type(gamma, None, numeric)
        self._parms["gamma"] = gamma


    @property
    def rank_ratio(self):
        """
        Desired rank of the ICF matrix expressed as an ration of number of input rows (-1 means use sqrt(#rows)).

        Type: ``float``  (default: ``-1``).
        """
        return self._parms.get("rank_ratio")

    @rank_ratio.setter
    def rank_ratio(self, rank_ratio):
        assert_is_type(rank_ratio, None, numeric)
        self._parms["rank_ratio"] = rank_ratio


    @property
    def positive_weight(self):
        """
        Weight of positive (+1) class of observations

        Type: ``float``  (default: ``1``).
        """
        return self._parms.get("positive_weight")

    @positive_weight.setter
    def positive_weight(self, positive_weight):
        assert_is_type(positive_weight, None, numeric)
        self._parms["positive_weight"] = positive_weight


    @property
    def negative_weight(self):
        """
        Weight of positive (-1) class of observations

        Type: ``float``  (default: ``1``).
        """
        return self._parms.get("negative_weight")

    @negative_weight.setter
    def negative_weight(self, negative_weight):
        assert_is_type(negative_weight, None, numeric)
        self._parms["negative_weight"] = negative_weight


    @property
    def disable_training_metrics(self):
        """
        Disable calculating training metrics (expensive on large datasets)

        Type: ``bool``  (default: ``True``).
        """
        return self._parms.get("disable_training_metrics")

    @disable_training_metrics.setter
    def disable_training_metrics(self, disable_training_metrics):
        assert_is_type(disable_training_metrics, None, bool)
        self._parms["disable_training_metrics"] = disable_training_metrics


    @property
    def sv_threshold(self):
        """
        Threshold for accepting a candidate observation into the set of support vectors

        Type: ``float``  (default: ``0.0001``).
        """
        return self._parms.get("sv_threshold")

    @sv_threshold.setter
    def sv_threshold(self, sv_threshold):
        assert_is_type(sv_threshold, None, numeric)
        self._parms["sv_threshold"] = sv_threshold


    @property
    def fact_threshold(self):
        """
        Convergence threshold of the Incomplete Cholesky Factorization (ICF)

        Type: ``float``  (default: ``1e-05``).
        """
        return self._parms.get("fact_threshold")

    @fact_threshold.setter
    def fact_threshold(self, fact_threshold):
        assert_is_type(fact_threshold, None, numeric)
        self._parms["fact_threshold"] = fact_threshold


    @property
    def feasible_threshold(self):
        """
        Convergence threshold for primal-dual residuals in the IPM iteration

        Type: ``float``  (default: ``0.001``).
        """
        return self._parms.get("feasible_threshold")

    @feasible_threshold.setter
    def feasible_threshold(self, feasible_threshold):
        assert_is_type(feasible_threshold, None, numeric)
        self._parms["feasible_threshold"] = feasible_threshold


    @property
    def surrogate_gap_threshold(self):
        """
        Feasibility criterion of the surrogate duality gap (eta)

        Type: ``float``  (default: ``0.001``).
        """
        return self._parms.get("surrogate_gap_threshold")

    @surrogate_gap_threshold.setter
    def surrogate_gap_threshold(self, surrogate_gap_threshold):
        assert_is_type(surrogate_gap_threshold, None, numeric)
        self._parms["surrogate_gap_threshold"] = surrogate_gap_threshold


    @property
    def mu_factor(self):
        """
        Increasing factor mu

        Type: ``float``  (default: ``10``).
        """
        return self._parms.get("mu_factor")

    @mu_factor.setter
    def mu_factor(self, mu_factor):
        assert_is_type(mu_factor, None, numeric)
        self._parms["mu_factor"] = mu_factor


    @property
    def max_iterations(self):
        """
        Maximum number of iteration of the algorithm

        Type: ``int``  (default: ``200``).
        """
        return self._parms.get("max_iterations")

    @max_iterations.setter
    def max_iterations(self, max_iterations):
        assert_is_type(max_iterations, None, int)
        self._parms["max_iterations"] = max_iterations


    @property
    def seed(self):
        """
        Seed for pseudo random number generator (if applicable)

        Type: ``int``  (default: ``-1``).
        """
        return self._parms.get("seed")

    @seed.setter
    def seed(self, seed):
        assert_is_type(seed, None, int)
        self._parms["seed"] = seed


