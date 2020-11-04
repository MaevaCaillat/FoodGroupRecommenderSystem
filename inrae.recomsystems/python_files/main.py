# -*- coding: utf-8 -*-
"""The main function.

@author: Maeva.Caillat

Run this module to run the whole code.

"""
import sys


from data import (nb_user,
                  nb_item,
                  gamma,
                  termination_value,
                  heuristic,
                  epsilon,
                  delta,
                  nb_experiment,
                  database,
                  nb_matrix,
                  nb_user_init_distrib,
                  israeli)
from heuristic_evaluation import heuristic_evaluation


# pylint: disable=C0103
"""MY_PATH_OUTPUTS = ('/home/mmip/Documents/Python/prefelicitgroup/'
                   + 'inrae.recomsystems/inrae.recomsystems/outputs/'
                   + 'results.txt')"""
"""MY_PATH_OUTPUTS = ('/Users/sonialementec/Documents/INRAE/Git/'
                   + 'inrae.recomsystems/inrae.recomsystems/outputs/'
                   + 'results.txt')"""
MY_PATH_OUTPUTS = ('C:/Users/maeva/Documents/Cours_ei4/INRAE/prefelicitgroup/'
                   + 'inrae.recomsystems/inrae.recomsystems/outputs/'
                   + 'results.txt')

nb_user_list = [5, 7, 10, 12, 15]

# Save a reference to the original standard output
original_stdout = sys.stdout

with open(MY_PATH_OUTPUTS, 'w') as f:
    # Change the standard output to the file we created.
    sys.stdout = f

    for i in nb_user_list:
        (dataset,
         percent_queried_array,
         runtime_per_query_array,
         nb_query_array,
         percent_queried_vars,
         runtime_per_query_vars,
         nb_query_vars,
         loss_array) = heuristic_evaluation(
             i,
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
             israeli)
        print('The heuristic: ', heuristic)
        print('The number of users: ', i)
        print('The number of items: ', nb_item)
        print('The percentages of dataset queried: ',
              percent_queried_array)
        print('The runtimes per query (seconds): ',
              runtime_per_query_array)
        print('The numbers of queries asked: ',
              nb_query_array)
        print('The variance of the number of queries asked: ',
              nb_query_vars)
        print('The expected losses: ', loss_array)
        print("\n")
    # Reset the standard output to its original value
    sys.stdout = original_stdout
