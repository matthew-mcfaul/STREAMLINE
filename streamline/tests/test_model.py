import os
import time
import optuna
import pytest
import shutil
import logging
from streamline.dataprep.eda_runner import EDARunner
from streamline.dataprep.data_process import DataProcessRunner
from streamline.featurefns.feature_runner import FeatureImportanceRunner
from streamline.featurefns.feature_runner import FeatureSelectionRunner
from streamline.modeling.modeljob import ModelJob
from streamline.models.logistic_regression import LogisticRegression
from streamline.models.naive_bayes import NaiveBayes


algorithms, run_parallel, output_path = ["MI", "MS"], False, "./tests/"
dataset_path, experiment_name = "./DemoData/", "demo",


def test_setup():
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    eda = EDARunner(dataset_path, output_path, experiment_name, exploration_list=None, plot_list=None,
                    class_label="Class", n_splits=5)
    eda.run(run_parallel=False)
    del eda

    dpr = DataProcessRunner(output_path, experiment_name)
    dpr.run(run_parallel=False)
    del dpr

    f_imp = FeatureImportanceRunner(output_path, experiment_name, algorithms=algorithms)
    f_imp.run(run_parallel=False)
    del f_imp

    f_sel = FeatureSelectionRunner(output_path, experiment_name, algorithms=algorithms)
    f_sel.run(run_parallel)


@pytest.mark.parametrize(
    ("model", ),
    [
        (LogisticRegression(), ),
        (NaiveBayes(), ),
    ],
)
def test_valid_models(model):

    start = time.time()

    logging.warning("Running " + model.small_name + " Model Optimization")

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    for i in range(1):
        model_job = ModelJob(output_path + '/' + experiment_name + '/demodata', output_path, experiment_name, i)
        model_job.run(model)
        # logging.warning("Best Params:" + str(model.params))
        model_job = ModelJob(output_path + '/' + experiment_name + '/hcc-data_example', output_path, experiment_name, i)
        model_job.run(model)
        # logging.warning("Best Params:" + str(model.params))
        model_job = ModelJob(output_path + '/' + experiment_name + '/hcc-data_example_no_covariates',
                             output_path, experiment_name, i)
        model_job.run(model)
        # logging.warning("Best Params:" + str(model.params))

    logging.warning(model.small_name + " Optimization Step, "
                                       "Time running" + "" + ": " + str(time.time() - start))

    # shutil.rmtree(output_path)