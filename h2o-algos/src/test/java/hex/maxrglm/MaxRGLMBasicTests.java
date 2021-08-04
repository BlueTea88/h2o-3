package hex.maxrglm;

import org.junit.Test;
import org.junit.runner.RunWith;
import water.Scope;
import water.fvec.Frame;
import water.runner.CloudSize;
import water.runner.H2ORunner;

import java.util.Arrays;
import java.util.stream.IntStream;

import static hex.genmodel.utils.MathUtils.combinatorial;
import static hex.glm.GLMModel.GLMParameters.Family.gaussian;
import static hex.maxrglm.MaxRGLMUtils.updatePredIndices;
import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertTrue;
import static water.TestUtil.assertEqualArrays;
import static water.TestUtil.parseTestFile;

@RunWith(H2ORunner.class)
@CloudSize(1)
public class MaxRGLMBasicTests {
    
    /***
     * test the combination name generation is correct for 4 predictors, 
     *  choosing 1 predictor only, 
     *           2 predictors only,
     *           3 predictors only
     *           4 predictors
     */
    @Test
    public void testColNamesCombo() {
        assertCorrectCombos(new Integer[][]{{0}, {1}, {2}, {3}}, 4, 1);
        assertCorrectCombos(new Integer[][]{{0,1}, {0,2}, {0,3}, {1,2}, {1,3}, {2,3}}, 4, 2);
        assertCorrectCombos(new Integer[][]{{0,1,2}, {0,1,3}, {0,2,3}, {1,2,3}}, 4, 3);
        assertCorrectCombos(new Integer[][]{{0,1,2,3}}, 4, 4);
    }
    
    public void assertCorrectCombos(Integer[][] answers, int maxPredNum, int predNum) {
        int[] predIndices = IntStream.range(0, predNum).toArray();
        int zeroBound = maxPredNum-predNum;
        int[] bounds = IntStream.range(zeroBound, maxPredNum).toArray();   // highest combo value
        int numModels = combinatorial(maxPredNum, predNum);
        for (int index = 0; index < numModels; index++) {    // generate one combo
            assertEqualArrays(Arrays.stream(predIndices).boxed().toArray(Integer[]::new), answers[index]);
            updatePredIndices(predIndices, bounds);
        }
    }
    
    // test the returned r2 are from the best predictors
    @Test
    public void testBestR2Prostate() {
        Scope.enter();
        try {
            double tol = 1e-6;
            Frame trainF = parseTestFile("smalldata/logreg/prostate.csv");
            Scope.track(trainF);
            MaxRGLMModel.MaxRGLMParameters parms = new MaxRGLMModel.MaxRGLMParameters();
            parms._response_column = "AGE";
            parms._family = gaussian;
            parms._ignored_columns = new String[]{"ID"};
            parms._max_predictor_number=1;
            parms._train = trainF._key;
            MaxRGLMModel model1 = new MaxRGLM(parms).trainModel().get();
            Scope.track_generic(model1); // best one predictor model
            
            parms._max_predictor_number=2;
            MaxRGLMModel model2 = new MaxRGLM(parms).trainModel().get();
            Scope.track_generic(model2); // best one and two predictors models
            assertTrue(Math.abs(model1._output._best_r2_values[0]-model2._output._best_r2_values[0]) < tol);
            
            parms._max_predictor_number=3;
            MaxRGLMModel model3 = new MaxRGLM(parms).trainModel().get();
            Scope.track_generic(model3); // best one, two and three predictors models
            assertTrue(Math.abs(model2._output._best_r2_values[1]-model3._output._best_r2_values[1]) < tol);
        } finally {
            Scope.exit();
        }
    }

}
