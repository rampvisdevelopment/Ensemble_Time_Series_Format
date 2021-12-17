import pandas as pd
from sandu.data_types import SensitivityInput
import json
import numpy as np
from typing import List, Tuple

"""
Parses an Ensemble Time Series Format (entz) data set to make sandu SensitivityInput objects for specified quantities.
in quantities_of_interest. 

The SensitivityInput objects are saved to json files which may be loaded into and used by the python package sandu.

If you have not used sandu before it will be helpful to consult the examples, at https://github.com/ErikRZH/sandu 
"""


def output_file_name(entz_in: str, index: str) -> str:
    """ Returns the name and path to file output_i.csv given i.

    Args:
        entz_in: String containing the location of a dataset in ensemble time series format.
        index: The index i used to identify the model evaluation.

    Returns:
        output_file_name: The name and path to file output_i.csv.
    """
    output_file_name = entz_in + "/output_" + str(index) + ".csv"
    return output_file_name


def make_dataframe(entz_in: str, quantities_of_interest: List[dict]) -> pd.DataFrame:
    """Gives a pandas dataframe of the type used by the sandu library for sensitivity analysis given a entz structure.

    Args:
        entz_in: String containing the location of a dataset in time series ensemble format.
        quantities_of_interest: List containing dictionaries with information needed to make SensitivityInput objects.
           One dictionary/entry corresponds to one quantity of interest.
            Dictionaries have keys,
            name: Name of the quantity, the SensitivtiyInput object is saved as: name_input.json
            mean: Column containing the mean of the quantity.
            variance: Column containing the variance of the quantity.

    Returns:
        df: dataframe containing parameters-quantity_of_interests_mean/variance
    """
    df = pd.read_csv(entz_in + "/parameters.csv")
    df_temp = pd.read_csv(entz_in + "/output_metadata.csv")
    desc = df_temp["description"]
    time_name = df_temp.loc[df_temp["description"] == "time_unit"]["output"].at[0]
    for quantity in quantities_of_interest:
        df[quantity["mean"]] = np.nan
        df[quantity["mean"]] = df[quantity["mean"]].astype(object)
        df[quantity["variance"]] = np.nan
        df[quantity["variance"]] = df[quantity["variance"]].astype(object)
        for i in df["index"]:
            print("index: ", i)
            # Sort the output time series by day and add them in the appropriate columns
            df.at[i, quantity["mean"]] = pd.read_csv(output_file_name(entz_in, i)).sort_values(time_name)[
                quantity["mean"]].tolist()
            df.at[i, quantity["variance"]] = pd.read_csv(output_file_name(entz_in, i)).sort_values(time_name)[
                quantity["variance"]].tolist()
    return df


def get_parameters_and_bounds(entz_in: str) -> Tuple[list, list]:
    """ Returns two lists needed by sandu, one containing the names and one the bounds of model parameters.

    Args:
        entz_in: String containing the location of a dataset in time series ensemble format.

    Returns:
        parameters: List of the names of the parameters, as required by sandu.
        bounds: List containing the lower and upper bounds of the parameters as [lower, upper],
            in the same order as the parameters list.
    """
    df = pd.read_csv(entz_in + "/parameters_metadata.csv")
    parameters = df["parameter"].to_list()
    bounds = get_bounds(entz_in, parameters)
    return parameters, bounds


def get_bounds(entz_in: str, parameters):
    """ Returns a list containing the bounds of model parameters.

    Args:
        entz_in: String containing the location of a dataset in time series ensemble format.
        parameters: List of the names of the parameters, as required by sandu.

    Returns:
        bounds: List containing the lower and upper bounds of the parameters as [lower, upper],
            in the same order as the parameters list.
    """
    df = pd.read_csv(entz_in + "/parameters.csv")
    bounds = []
    for parameter in parameters:
        upper_bound = df[parameter].max().item()
        lower_bound = df[parameter].min().item()
        bounds_entry = [lower_bound, upper_bound] if upper_bound != lower_bound else [upper_bound]
        bounds.append(bounds_entry)
    return bounds


# The quantity_mean and quantity_variance values used for
quantities_of_interest = [{"name": "inc_case", "mean": "inc_case_mean", "variance": "inc_case_var"},
                          {"name": "age_7_H", "mean": "age_7_H_mean", "variance": "age_7_H_var"}]
location = "../entz_example_dataset"

df = make_dataframe(location, quantities_of_interest)
parameters, bounds = get_parameters_and_bounds(location)

for quantity in quantities_of_interest:
    new_sensitivity_input = SensitivityInput(df.to_json(index=False, orient="split"), parameters, bounds,
                                             quantity["mean"], quantity["variance"])
    with open(quantity["name"] + "_input.json", "w", encoding="utf-8") as f:
        json.dump(new_sensitivity_input.__dict__, f, ensure_ascii=False, indent=4)

    # Open and load every object to validate it
    with open(quantity["name"] + "_input.json", "r") as read_file:
        x = json.load(read_file, object_hook=lambda d: SensitivityInput(**d))

print(x.df())
