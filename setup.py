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


from setuptools import setup
from pathlib import Path

README = Path(__file__).parent / "README.rst"

setup(
    name="hiplot-mlflow",
    description="HiPlot fetcher plugin for MLflow experiment tracking.",
    long_description=README.read_text(),
    url="https://github.com/facultyai/hiplot-mlflow",
    author="Faculty",
    author_email="opensource@faculty.ai",
    license="Apache Software License",
    py_modules=["hiplot_mlflow"],
    setup_requires=["setuptools_scm"],
    install_requires=["hiplot", "mlflow", "numpy"],
    extras_require={
        "dev": [
            "black==22.3.0",
            "flake8",
            "flake8-black",
            "mypy",
            "pytest",
            "tox",
        ]
    },
)
