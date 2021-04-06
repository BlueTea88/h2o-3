setwd(normalizePath(dirname(R.utils::commandArgs(asValues=TRUE)$"f")))
source("../../../scripts/h2o-r-test-setup.R")

# test to show that we can call gbm with x = infogram model
infogramIrisGBM <- function() {
    bhexFV <- h2o.importFile(locate("smalldata/admissibleml_test/irisROriginal.csv"))
    bhexFV["Species"]<- h2o.asfactor(bhexFV["Species"])
    Y <- "Species"
    X <- c("Sepal.Length","Sepal.Width","Petal.Length","Petal.Width")
    Log.info("Build the model")
    mFV <- h2o.infogram(y=Y, x=X, training_frame=bhexFV,  seed=12345, ntop=50, model_algorithm='gbm')
    infogramsc <- mFV@model$scoring_history$training_rmse
    manualModel <- h2o.gbm(y=Y, x=mFV, training_frame=bhexFV, seed=12345)
    msc <- manualModel@model$scoring_history$training_rmse
    expect_equal(infogramsc, msc, tolerance=1e-6) # result should agree
}

doTest("Infogram: Iris core infogram with gbm as final model", infogramIrisGBM)
