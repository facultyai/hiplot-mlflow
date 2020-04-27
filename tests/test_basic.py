# Copyright 2020 Faculty Science Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

import hiplot
from pandas import DataFrame

import hiplot_mlflow
import pytest

RUN_ID_1 = str(uuid.uuid4())
RUN_ID_2 = str(uuid.uuid4())

SEARCH_RUNS_RESULT = DataFrame(
    {
        "run_id": [RUN_ID_1, RUN_ID_2],
        "params.numeric": [0, 1],
        "params.category": ["value1", "value2"],
        "metrics.third": [2, 4],
        "tags.test": ["yes", "no"],
    }
)
EXPERIMENT = hiplot.Experiment(
    [
        hiplot.Datapoint(
            uid=RUN_ID_1,
            values={
                "params.numeric": 0,
                "params.category": "value1",
                "metrics.third": 2,
            },
        ),
        hiplot.Datapoint(
            uid=RUN_ID_2,
            values={
                "params.numeric": 1,
                "params.category": "value2",
                "metrics.third": 4,
            },
        ),
    ]
)
EXPERIMENT_WITH_TAGS = hiplot.Experiment(
    [
        hiplot.Datapoint(
            uid=RUN_ID_1,
            values={
                "params.numeric": 0,
                "params.category": "value1",
                "metrics.third": 2,
                "tags.test": "yes",
            },
        ),
        hiplot.Datapoint(
            uid=RUN_ID_2,
            values={
                "params.numeric": 1,
                "params.category": "value2",
                "metrics.third": 4,
                "tags.test": "no",
            },
        ),
    ]
)


def test_wrong_schema():
    """Test passing unsupported schema.
    """
    with pytest.raises(hiplot.ExperimentFetcherDoesntApply):
        hiplot_mlflow.fetch_by_uri("something://")


def test_unsupported_reference_type():
    """Test passing correct schema and unsupported reference type.
    """
    with pytest.raises(hiplot.ExperimentValidationError):
        hiplot_mlflow.fetch_by_uri(f"mlflow://something/else")


@pytest.mark.parametrize(
    "include_tags, expected_result",
    [(False, EXPERIMENT), (True, EXPERIMENT_WITH_TAGS)],
)
def test_dataframe_to_experiment(include_tags, expected_result):
    """Test the conversion from dataframe to HiPlot experiment,
    with or without tags.
    """
    experiment = hiplot_mlflow._create_experiment_from_dataframe(
        SEARCH_RUNS_RESULT, include_tags
    )
    for test_dp, exp_dp in zip(
        experiment.datapoints, expected_result.datapoints
    ):
        assert test_dp.uid == exp_dp.uid
        assert test_dp.values == exp_dp.values
