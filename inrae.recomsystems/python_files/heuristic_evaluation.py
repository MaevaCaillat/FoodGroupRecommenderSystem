# -*- coding: utf-8 -*-
"""Computing the performances of the heuristics.

@author: Maeva.Caillat

"""

from itertools import permutations
import sys
import numpy as np
import pandas as pd
from datasets import dataset_random, fixed_dataset_sushi, random_dataset_sushi
from find_preferences import find_preferences
from data import MY_PATH_SUSHI

"""MY_PATH_TEMP_OUTPUTS = ('/home/mmip/Documents/Python/prefelicitgroup/'
                        + 'inrae.recomsystems/inrae.recomsystems/outputs/'
                        + 'temp_results.txt')"""
"""MY_PATH_TEMP_OUTPUTS = ('/Users/sonialementec/Documents/INRAE/Git/'
                        + 'inrae.recomsystems/inrae.recomsystems/outputs/'
                        + 'temp_results.txt')"""
MY_PATH_TEMP_OUTPUTS = ('C:/Users/maeva/Documents/Cours_ei4/INRAE/prefelicitgroup/'
                        + 'inrae.recomsystems/inrae.recomsystems/outputs/'
                        + 'temp_results.txt')

# pylint: disable=C0103
def heuristic_evaluation(nb_user,
                         nb_item,
                         gamma,
                         heuristic,
                         termination_value,
                         epsilon,
                         delta,
                         nb_experiment,
                         database,
                         nb_matrix,
                         nb_user_init_distrib,
                         israeli):
    """
    Return the performance criteria of heuritics.

    Parameters
    ----------
    nb_user : INT
        Number of users.
    nb_item : INT
        Numbers of items.
    gamma : INT
        Sample size for PrWin.
    heuristic : STRING
        Name of the heuristic.
    termination_value : FLOAT
        Termination value for the expected loss.
    epsilon : FLOAT
        Desired threeshold for EU loss.
    delta : FLOAT
        Confidence parameter.
    nb_experiment : INT
        Number of experiments (because IGB and ESB use sampling).
    database : STRING
        Dataset used (random, sushi or netflix).
    nb_matrix : INT
        Number of matrices needed for generating
        an initial permutation distribution for the sushi dataset.
    nb_user_init_distrib : INT
        Number of users needed for generating
        an initial permutation distribution for the sushi dataset.
    israeli : BOOL
        If israeli=True, apply the Israeli methods
        else, use the expected loss too.

    Returns
    -------
    dataset : ARRAY
        Array of nb_user * nb_item * nb_table.
    np.array(percent_queried_means) : ARRAY
        The mean of percentage of dataset queried.
    np.array(runtime_per_query_means) : ARRAY
        The mean runtime per query.
    np.array(nb_query_means) : ARRAY
        The mean number of queries.
    np.array(percent_queried_vars) : ARRAY
        The variance of the percentage of dataset queried.
    np.array(runtime_per_query_vars) : ARRAY
        The variance of the runtime per query.
    np.array(nb_query_vars) : ARRAY
        The variance of the number of queries.

    """
    # Save a reference to the original standard output
    original_stdout = sys.stdout

    with open(MY_PATH_TEMP_OUTPUTS, 'w') as f:
        # Change the standard output to the file we created.
        sys.stdout = f

        percent_queried_means = []
        runtime_per_query_means = []
        nb_query_means = []
        percent_queried_vars = []
        runtime_per_query_vars = []
        nb_query_vars = []
        loss_array = np.zeros(int(nb_user*nb_item*(nb_item-1)/2))

        if database == 'fixed_sushi':
            df_rating, distrib = fixed_dataset_sushi(nb_user,
                                                     nb_item,
                                                     nb_matrix,
                                                     nb_user_init_distrib,
                                                     MY_PATH_SUSHI)
        elif database == 'random_sushi':
            df_rating, distrib = random_dataset_sushi(nb_user,
                                                      nb_item,
                                                      nb_matrix,
                                                      nb_user_init_distrib,
                                                      MY_PATH_SUSHI)
        elif database == 'random':
            df_rating, distrib = dataset_random(nb_user, nb_item)
        else:
            raise ValueError("Invalid database")
        percent_queried_interm = []
        runtime_per_query_interm = []
        nb_query_interm = []

        for k in range(nb_experiment):
            print('Experiment', k)
            # Id of the users
            df_user_id = pd.DataFrame(np.array(range(df_rating.shape[0])))
            # The set of votdataers
            v = np.array(df_user_id).flatten()
            # The rankings of the candidates by the users
            rating = np.array(df_rating)
            # The set of candidate items
            c = np.arange(len(rating[0]))
            # The set of possible permutations
            vc = np.array(list(permutations(c)))
            (nw,
             runtime,
             percent_queried,
             loss,
             time_array,
             nb_queries) = find_preferences(v,
                                            c,
                                            vc,
                                            gamma,
                                            rating,
                                            distrib,
                                            heuristic,
                                            termination_value,
                                            epsilon,
                                            delta,
                                            israeli)
            print('A first necessary winner for %s and %s users is candidate'
                  % (heuristic, nb_user), nw)
            print('Runtime = % seconds' % runtime)
            print('%s cuts the communication up to %s percent'
                  % (heuristic, percent_queried))
            print("\n")
            percent_queried_interm.append(percent_queried)
            runtime_per_query_interm.append(runtime/nb_queries)
            nb_query_interm.append(nb_queries)
            loss_array[:len(loss)] += loss

        percent_queried_means.append(np.mean(percent_queried_interm))
        runtime_per_query_means.append(np.mean(runtime_per_query_interm))
        nb_query_means.append(np.mean(nb_query_interm))

        percent_queried_vars.append(np.var(percent_queried_interm))
        runtime_per_query_vars.append(np.var(runtime_per_query_interm))
        nb_query_vars.append(np.var(nb_query_interm))
        loss_array /= nb_experiment

        dataset = np.array([
            nb_user * nb_item
                ])
    # Reset the standard output to its original value
    sys.stdout = original_stdout

    return(dataset,
           np.array(percent_queried_means),
           np.array(runtime_per_query_means),
           np.array(nb_query_means),
           np.array(percent_queried_vars),
           np.array(runtime_per_query_vars),
           np.array(nb_query_vars),
           loss_array)
