setwd(normalizePath(dirname(R.utils::commandArgs(asValues=TRUE)$"f")))
source("../../../scripts/h2o-r-test-setup.R")

# tests that infogram build the correct model for core infogram.  Make sure 
# 1. it gets the correct result compared to deep's code.
# 2. the relevance and cmi frame contains the correct values
infogramIris <- function() {
    bhexFV <- h2o.importFile(locate("smalldata/admissibleml_test/irisROriginal.csv"))
    bhexFV["Species"]<- h2o.asfactor(bhexFV["Species"])
    Y <- "Species"
    X <- c("Sepal.Length","Sepal.Width","Petal.Length","Petal.Width")
    deepRel <- sort(c(0.009010006, 0.011170417, 0.755170945, 1.000000000))
    deepCMI <- sort(c(0.1038524, 0.7135458, 0.5745915, 1.0000000))
    Log.info("Build the model")
    browser()
    mFV <- h2o.infogram(y=Y, x=X, training_frame=bhexFV,  seed=12345, top_n_features=50)
    relCMIFrame <- h2o.get_relevance_cmi_frame(mFV) # get frames containing relevance and cmi
    frameCMI <- sort(as.vector(t(relCMIFrame[,3])))
    frameRel <- sort(as.vector(t(relCMIFrame[,2])))
    allCMI <- h2o.get_all_predictor_cmi(mFV)
    allRel <- h2o.get_all_predictor_relevance(mFV)
    admissibleCMI <- sort(h2o.get_admissible_cmi(mFV))
    admissibleRel <- sort(h2o.get_admissible_relevance(mFV))
    
    expect_equal(deepCMI, sort(allCMI), tolerance=1e-6) # check with Deep's result
    expect_equal(deepRel, sort(allRel), tolerance=1e-6) 
    expect_equal(sort(allCMI), frameCMI, tolerance=1e-6) # check relevance and cmi from frame agree with Deep's
    expect_equal(sort(allRel), frameRel, tolerance=1e-6) 
    expect_true(sum(admissibleCMI >= 0.1)==length(admissibleCMI)) # check and make sure relevance and cmi >= thresholds
    expect_true(sum(admissibleRel >= 0.1)==length(admissibleRel))
}

doTest("Infogram: Iris core infogram", infogramIris)
