# HiPlot-MLflow

A  [HiPlot](https://facebookresearch.github.io/hiplot/index.html) experiment fetcher plugin
for [MLflow](https://mlflow.org/), to help visualise your tracked experiments.

## Usage

### Installation

Install this library with `pip` as:

```Shell
pip install hiplot_mlflow
```

### Visualisation

You can visualise experiments either in a Jupyter notebook or using HiPLot's built in server.

This library implements an [experiment fetcher](https://facebookresearch.github.io/hiplot/tuto_webserver.html#experiments-uri)
using the `mlflow://` schema. After the schema you can use eitherthe experiment number, or name:

```text
mlflow://id/0
mlflow://name/experiment-name
```

You can also use query strings to modify the returned results. Currently the library
supports these options:

* `tag`: setting it to any value enables returning all the tags as well (by
  default only `params` and `metrics` are returned). For example: `mlflow://id/0?tags=yes`


There are also options to look up experiments directly by ID or name, and thus all
the forms that you can use to fetch experiments are:

```Python
import hiplot_mlflow
# by name
experiment = hiplot_mlflow.fetch("experiment-name")
# or by ID
experiment = hiplot_mlflow.fetch_by_id(0)
# or by URI, either using the ID or name format
experiment = hiplot_mlflow.fetch_by_uri("mlflow://id/0")
```

You can enable reporting tags when calling these functions by
setting `include_tag=True`.

#### Notebooks

When in a notebook, you most likely want to use the `hiplot_mlflow.fetch`
function for simplicity, fetching results by experiment name:

```Python
import hiplot_mlflow
experiments = hiplot_mlflow.fetch("my-lovely-experuments")
# Display the fetched experiments in the window
experiments.display(force_full_width=True)
```

![Loading HiPLot in a notebook](images/notebook_name.png)

See more about what you can do with the returned `hiplot.Experiment` values in the
[HiPlot documentation](https://facebookresearch.github.io/hiplot/experiment_settings.html).

#### Built in server

To use [HiPlot's built in webserver](https://facebookresearch.github.io/hiplot/tuto_webserver.html),
you can start it up with this custom fetcher loaded:

```Shell
hiplot hiplot_mlflow.fetch_by_uri
```

Then can use either the previous full URI format to load your experiments.

![Loading HiPlot server with experiment name](images/server_name.png)

You can also use the [multiple experiments](https://facebookresearch.github.io/hiplot/tuto_webserver.html#compare-multiple-experiments)
loading syntax as well. Either the dictionary format (to define your own labels):

```text
multi://{
    "first-experiment": "mlflow://id/1",
    "another-experiment": "mlflow://name/another-experiment?tags=yes"
}
```

or list format:

```text
multi://[
    "mlflow://id/1",
    "mlflow://name/another-experiment?tags=yes"
]
```

![Multiple experiments in HiPlot server](images/server_multi.png)
