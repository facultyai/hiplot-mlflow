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
from typing import Any
from urllib.parse import parse_qs, urlparse

import hiplot
from mlflow import search_runs, tracking
from mlflow.exceptions import MlflowException
from numpy import isfinite
from pandas import DataFrame


def fetch(name: str, include_tags: bool = False) -> hiplot.Experiment:
    """Fetch MLflow experiment by name.

    Parameters
    ----------
    name: str
        The name of the tracked experiment to look up
    include_tags: bool, optional
        Whether to include tags in the resulting HiPlot experiment (False)

    Returns
    -------
    hiplot.Experiment
        The resulting experiment
    """
    return fetch_by_id(_get_experiment_id_from_name(name), include_tags)


def fetch_by_id(id: Any, include_tags: bool = False) -> hiplot.Experiment:
    """Fetch MLFlow experiment by ID.

    Parameters
    ----------
    id: int or str
        The ID if the experiment to look up
    include_tags: bool, optional
        Whether to include tags in the resulting HiPlot experiment (False)

    Returns
    -------
    hiplot.Experiment
        The resulting experiment
    """
    try:
        df = search_runs([id])
    except MlflowException as e:
        raise hiplot.ExperimentValidationError(str(e))
    return _create_experiment_from_dataframe(df, include_tags)


def fetch_by_uri(uri: str) -> hiplot.Experiment:
    """Fetch MLflow experiment using URI.

    The URI can take these forms:
    * ``mlflow://id/<id>`` to look up experiments by ID
    * ``mlflow://name/<name>`` to look up experiments by name

    You can also add a query string to modify the results:
    * Setting ``tags`` to any value will return results with
      tags included. For example: ``mlflow://id/<id>?tags=yes``

    Parameters
    ----------
    uri: str
        The fetcher URI to use

    Returns
    -------
    hiplot.Experiment
        The resulting experiment
    """
    # Only apply this fetcher if the URI matches our schema
    parsed_uri = urlparse(uri)
    if parsed_uri.scheme != "mlflow":
        raise hiplot.ExperimentFetcherDoesntApply()

    reference_type = parsed_uri.netloc
    reference = parsed_uri.path.strip("/")
    include_tags = parse_qs(parsed_uri.query).get("tags") is not None
    if reference_type == "name":
        return fetch(reference, include_tags)
    elif reference_type == "id":
        return fetch_by_id(reference, include_tags)
    else:
        raise hiplot.ExperimentValidationError()


def _get_experiment_id_from_name(name: str) -> Any:
    """Get an MLflow experiment's ID from its name
    """
    client = tracking.MlflowClient()
    experiment = client.get_experiment_by_name(name)
    if experiment is None:
        raise hiplot.ExperimentValidationError()
    return experiment.experiment_id


def _create_experiment_from_dataframe(
    df: DataFrame, include_tags: bool
) -> hiplot.Experiment:
    """Generate HiPlot experiment from MLFlow runs.

    Parameters
    ----------
    df: pandas.DataFrame
        A dataframe (returned by ``mlflow.search_runs`` normally)
        to turn process
    include_tags: bool
        Whether or not to include tags in the results (False)

    Returns
    -------
    hiplot.Experiment
        The processed experiment
    """
    exp = hiplot.Experiment()
    params = [p for p in df.columns if p.startswith("params.")]
    metrics = [m for m in df.columns if m.startswith("metrics.")]
    if include_tags:
        tags = [t for t in df.columns if t.startswith("tags.")]
    for _, row in df.iterrows():
        values = {}
        for p in params:
            values[p] = row[p]

        for m in metrics:
            if isfinite(row[m]):
                values[m] = row[m]

        if include_tags:
            for t in tags:
                values[t] = row[t]

        dp = hiplot.Datapoint(
            uid=str(uuid.UUID(row["run_id"])), values=values,
        )
        exp.datapoints.append(dp)
    return exp
