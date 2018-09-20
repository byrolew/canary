# Canary Anomaly Detection

This is a research prototype built as part of an internship project. 
See the bug [1475933](https://bugzilla.mozilla.org/showdependencytree.cgi?id=1475933&hide_resolved=1) 
for context.

## Installation

You should just install the requirements:
```bash
pip install -e .
```

## Testing

You can run tests by typing `pytest` in the `canary` directory.

## Generator
The generator module is use to generate the test data, i.e. data with synthetic anomalies. 
The Data flow:
1. Download the data with `download_whole.py`, eg:
    ```bash
    python canary/generator/download/download_whole.py /some/directory --nightly_version_number 5
    ``` 
    The script makes catalogs in `/some/directory` (first argument)  with the data from 5 (second argument) 
    latest versions of nightly. The data is downloaded from Telemetry 
    [HTTP API](https://github.com/mozilla/python_mozaggregator#api)
2. Generate the data with anomalies with `generate_test_data.py`, eg:
    ```bash
    python canary/generator/generate_test_data.py example_data/*.json /some/directory --plots
    ```
    The first argument is the directory with downloaded data. In the example `example_data` from the module 
    is used. The second argument indicates the directory, where the generated data is saved. 
    The `--plots` flag specifies that the plots should be saved.
    
    What's actually happening to the data inside:
    * The data is preprocessed and split into train and test set. The `y` is generated on the assumption, 
    that there are no anomalies in the data set. The train set won't be changed.
    * The test set is changed by the pipelines, which are in `pipelines_*.py`. Each pipeline consists
    of some transformers, that are in `transformers` directory. Each pipeline (and each transformer) operates
    only on some kinds of the histograms. Some of the transformers add anomalies and change `y` and some only 
    add noise or trend.
    * The plots of changes are generated with usage of the `save_plot` function from `utils`.
    * Everything is saved in the directory provided by the user. In our example `/some/directory`.
3. Download the data split by every dimension with `download_split.py`, eg:
    ```bash
    python canary/generator/download/download_split.py /some/directory --channel nightly --number_of_versions 5
    ```
    The script makes catalogs in `/some/directory` (first argument) with the data from 5 
    (`--number_of_versions` argument) latest versions of nightly (`--channel` argument). 
    The data is downloaded from Telemetry [HTTP API](https://github.com/mozilla/python_mozaggregator#api)
4. Generate the split data with anomalies with `generate_anomalies_in_split_data.py`, eg:
    ```bash
    python canary/generator/generate_anomalies_in_split_data.py generated/data/*.json \
    --split_data_dir example_data_split/*.json --output_dir /save/directory
    ```
    - The first argument is the directory with data generated with `generate_test_data.py`. 
    - The `--split_data_dir` argument is the directory with the data downloaded with `download_split.py`, 
    here example data, which is in the repo is used.
    - The `--output_dir` argument indicates the directory, where the generated data is saved. 
    
    The script saves four files with the data. Two aggregated by architecture: original and with 
    anomalies and two aggregated by os: original and with anomalies.

## Notebooks with models

At the top of the notebooks the path to the files with data should be adapted. 
The rest of the notebooks should work after package installation.

There are three notebooks in the `model` directory:
 - `Statistical.ipynb` contains the Statistical Model with the results.
 - `LSTM_on_distances.ipynb` contains the Neural Network Model working on the distances.
 - `Anomaly_Explanation.ipynb` contains the example explanations of some anomalies.

