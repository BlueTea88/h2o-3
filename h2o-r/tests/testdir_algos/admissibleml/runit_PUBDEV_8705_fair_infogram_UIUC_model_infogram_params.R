setwd(normalizePath(dirname(R.utils::commandArgs(asValues=TRUE)$"f")))
source("../../../scripts/h2o-r-test-setup.R")

# tests that infogram build the correct model for fair infogram.  Make sure 
# 1. it gets the correct result compared to deep's code.
# 2. the relevance and cmi frame contains the correct values
# 3. test that infogram_algorithm_params work
# 4. test that model_algorithm_params work.
infogramUIUC <- function() {
    bhexFV <- h2o.importFile(locate("smalldata/admissibleml_test/taiwan_credit_card_uci.csv"))
    bhexFV["default payment next month"]<- h2o.asfactor(bhexFV["default payment next month"])
    Y <- "default payment next month"
    X <- c("LIMIT_BAL", "EDUCATION", "MARRIAGE",
           "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6", "BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4",
           "BILL_AMT5", "BILL_AMT6", "PAY_AMT1", "PAY_AMT2", "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6")
    deepRel <- sort(c(0.07893684, 0.01800647, 0.01098464, 1.00000000, 0.17214091, 0.05758034, 
                      0.03805165, 0.03097822, 0.03125514, 0.06620615, 0.02368234, 0.01071032, 0.01051331, 0.02224472, 
                      0.01574407, 0.02323453, 0.01780084, 0.01759464, 0.01063546, 0.01165965, 0.01447185))
    deepCMI <- sort(c(0.25225589, 0.04838205, 0.02515363, 1.00000000, 0.65011528, 0.49968050, 
                      0.44469423, 0.41195756, 0.35604507, 0.14960576, 0.11973009, 0.10654662, 0.12172179, 0.12809776, 
                      0.11255243, 0.28748429, 0.24735238, 0.23491307, 0.19843329, 0.17768404, 0.17737053))
    Log.info("Build the model")
    mFV <- h2o.infogram(y=Y, x=X, training_frame=bhexFV,  seed=12345, ntop=50, sensitive_attributes = c("SEX", "AGE"))
    relCMIFrame <- h2o.get_relevance_cmi_frame(mFV) # get frames containing relevance and cmi
    frameCMI <- sort(as.vector(t(relCMIFrame[,3])))
    frameRel <- sort(as.vector(t(relCMIFrame[,2])))
    allCMI <- h2o.get_all_predictor_cmi(mFV)
    allRel <- h2o.get_all_predictor_relevance(mFV)
    admissibleCMI <- sort(h2o.get_admissible_cmi(mFV))
    admissibleRel <- sort(h2o.get_admissible_relevance(mFV))
    
    expect_equal(deepCMI, sort(allCMI), tolerance=1e-6) # Deep's result is problematic due to building same model with different predictors orders
    expect_equal(deepRel, sort(allRel), tolerance=1e-6) 
    expect_equal(sort(allCMI), frameCMI, tolerance=1e-6) # check relevance and cmi from frame agree with Deep's
    expect_equal(sort(allRel), frameRel, tolerance=1e-6) 
    expect_true(sum(admissibleCMI >= 0.1)==length(admissibleCMI)) # check and make sure relevance and cmi >= thresholds
    expect_true(sum(admissibleRel >= 0.1)==length(admissibleRel))
    
    # model built with different parameters and their relevance and cmi to be different
    gbm_params <- list(ntrees=3)
    glm_params <- list(family='binomial')
    
    mFVNew <- h2o.infogram(y=Y, x=X, training_frame=bhexFV,  seed=12345, ntop=50, infogram_algorithm='gbm', 
                           infogram_algorithm_params=gbm_params, model_algorithm='glm', model_algorithm_params=glm_params)
    admissibleCMINew <- sort(h2o.get_admissible_cmi(mFVNew))
    admissibleRelNew <- sort(h2o.get_admissible_relevance(mFVNew))
    expect_true((admissibleCMINew[1] - admissibleCMI[1]) > 0.1) # CMI and relevance should not equal
    expect_true((admissibleRelNew[1] - admissibleRel[1]) > 0.1)
}

doTest("Infogram: UIUC data fair infogram", infogramUIUC)
