# -*- coding: utf-8 -*-
"""Finding a winning candidate.

@author: Maeva.Caillat

"""

import timeit
import sys
import numpy as np
from other_useful_functions import (deterministic_answers_to_query,
                                    transitivity_complete)
from borda_voting_protocol import borda, borda_permut
from expected_loss import expected_loss
from igb import optimal_wig_query
from esb import optimal_wem_query
from evoi import optimal_evoi_query_no_mc


# pylint: disable=C0103
def find_preferences(v,
                     c,
                     vc,
                     gamma,
                     rating,
                     distrib,
                     heuristic,
                     termination_value,
                     epsilon,
                     delta,
                     israeli):
    """
    Return a winning candidate thanks a given heuristic.

    Parameters
    ----------
    v : ARRAY
        The set of voters.
    c : ARRAY
        The set of candidates.
    vc : ARRAY
        The set of permutations.
    gamma : INT
        The sample size for PrWin algo.
    rating : ARRAY
        The rankings of the candidates by the users.
    heuristic : STRING
        The heuristic used to find a winner.
    termination_value : FLOAT
        The algo stops when EU loss is higher than this value.
    epsilon : FLOAT
        The desired threeshold for EU loss,
        used to calculate the sample size for EU loss.
    delta : FLOAT
        The confidence parameter (often 95% or 99%).
    database : STRING
        Dataset used (random, sushi or netflix).
    nb_matrix : INT
        Number of matrices needed for generating
        an initial permutation distribution for the sushi dataset.
    nb_user_init_distrib : INT
        Number of users needed for generating
        an initial permutation distribution for the sushi dataset.
    israeli : BOOL
        If True, apply the Israeli methods else, use the expected loss too.

    Returns
    -------
    nw : INT
        A necessary winner.
    runtime : TIME
        Total runtime in seconds.
    communication_cut : FLOAT
        Percentage of dataset queried.
    loss_array : ARRAY
        The expected loss array.
    time_array : ARRAY
        The array of time when expected losses are saved.
    nb_queries : INT
        Number of queries.

    """
    # Initialize time.
    starttime = timeit.default_timer()

    # The initial possible maximums of items.
    p_max = np.ones(len(c)) * ((len(c)-1) * len(v))

    # The initial possible minimums of items.
    p_min = np.zeros(len(c))

    # The list of possible winners.
    nw_list = []

    # The list of queries asked.
    queries = []

    # The real Borda scores.
    eu_array = np.array(list(borda(rating).values()))
    print("The real expected Borda scores are: ", eu_array)

    # Stopping criterion booleans.
    stop_loss = True
    stop_nw = True
    stopping_criterion = True

    # If we want to compute the expected loss.
    if not israeli:
        # The worst case loss.
        # x = (len(c) - 1) * len(v) - max(eu_array)
        # Minimum number of samples needed.
        n = 1000
        # n = int(round((x ** 2) / ((epsilon ** 2) * delta))) + 1
        print('Number of samples needed:', n)
        # The expected loss.
        expect_loss = expected_loss(v, c, vc, n, distrib)
        print("The initial expected loss is: ", expect_loss)

        # The expected losses vs. time.
        expect_losses = [expect_loss]

    nb_queries = 0
    # The list of least-liked items for every item and every voter.
    list_alternative_worst = [[[] for _ in range(len(c))]
                              for _ in range(len(v))]
    time = [timeit.default_timer()]
    print("\n")
    while stopping_criterion:
        # Find the next query qi,j,k thanks to an heuristic.

        # Highest Expected Score Heuristic for Borda Voting
        if heuristic == 'ESB':
            query, value_query = optimal_wem_query(v,
                                                   c,
                                                   vc,
                                                   gamma,
                                                   distrib,
                                                   queries)
        # Information Gain Heuristic for Borda Voting
        elif heuristic == 'IGB':
            query, value_query = optimal_wig_query(v,
                                                   c,
                                                   vc,
                                                   gamma,
                                                   distrib,
                                                   queries)
        # Expected Value of Information Heuristic for Borda Voting
        elif heuristic == 'EVOI':
            query, value_query = optimal_evoi_query_no_mc(v,
                                                          c,
                                                          vc,
                                                          distrib,
                                                          queries)
        # EVOI heuristic, then IGB heuristic if EVOI=0
        elif heuristic == 'EVOI+IGB':
            query, value_query = optimal_evoi_query_no_mc(v,
                                                          c,
                                                          vc,
                                                          distrib,
                                                          queries)
            if value_query == 0:
                query, value_query = optimal_wig_query(v,
                                                       c,
                                                       vc,
                                                       gamma,
                                                       distrib,
                                                       queries)
        else:
            sys.exit('Error in the name of the heuristic!')

        vi = query[0]
        cj = query[1]
        ck = query[2]
        query = [vi, cj, ck]
        print("The question selected is: \'User v"
              + str(vi) + ", do you prefer c"
              + str(cj) + " or c"
              + str(ck) + "? \'")

        # If query not already asked.
        if query not in queries:
            # Add the query to list of queries.
            queries.append(query)
            nb_queries += 1
            # We ask user vi to answer cj>ck.
            answer = deterministic_answers_to_query(vi, cj, ck, rating)
            # We use transitivity closure in answers to queries.
            (p_min,
             p_max,
             distrib,
             queries,
             list_alternative_worst) = transitivity_complete(answer,
                                                             vi,
                                                             cj,
                                                             ck,
                                                             p_min,
                                                             p_max,
                                                             vc,
                                                             distrib,
                                                             queries,
                                                             list_alternative_worst)
            print("Pmax = ", p_max)
            print("Pmin = ", p_min)

            # Update the possible winner array.
            nw_list = [j for j in range(len(c))
                       if p_min[j] >= max(np.delete(p_max, j))]
            # False if no approximate winner, True otherwise.
            stop_nw = (not nw_list)
            print("Number of different questions asked: ", nb_queries)

            if not israeli:
                # The current expected Borda scores.
                eu_array = np.array(list(borda_permut(distrib, vc).values()))
                # The worst case loss.
                # x = (len(c) - 1) * len(v) - max(eu_array)
                # Minimum number of samples needed.
                n = 1000
                # n = int(round((x ** 2) / ((epsilon ** 2) * delta)))+1
                print('Number of samples needed:', n)
                # The expected loss.
                expect_loss = expected_loss(v, c, vc, n, distrib)
                expect_losses.append(expect_loss)
                print("Current EU: ", eu_array)
                print("Current expected loss: ", expect_loss)
                stop_loss = np.any(expect_loss > termination_value)

            stopping_criterion = (stop_loss and stop_nw)
            time.append(timeit.default_timer())
            print("\n")

        else:
            print("Question already asked before.")
            print("\n")
    # if a possible winner is found, return it.
    if not stop_nw:
        nw = nw_list[0]
    # if the expected loss is null, return the item with the best expected score.
    else:
        nw = np.argmax(eu_array)

    runtime = timeit.default_timer() - starttime
    # The cut in the communication cost.
    communication_cut = 100 * (1 - (2*nb_queries/(len(c)*len(v)*(len(c)-1))))
    time_array = np.array(time)-starttime

    if israeli:
        return(nw,
               runtime,
               communication_cut,
               np.array([]),
               time_array,
               nb_queries)

    return(nw,
           runtime,
           communication_cut,
           np.array(expect_losses),
           time_array,
           nb_queries)
