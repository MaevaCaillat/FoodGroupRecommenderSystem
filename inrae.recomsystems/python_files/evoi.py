# -*- coding: utf-8 -*-
"""The Expected Value of Information heuristic (EVOI).

@author: Maeva.Caillat

This module implements the EVOI heuristic.

"""
from itertools import permutations, combinations
import re
import numpy as np
from numpy import random as rd
from other_useful_functions import posterior_distrib, proba_query
from borda_voting_protocol import borda_permut


# pylint: disable=C0103
def expected_value_no_mc(v, c, vc, init_distrib):
    """
    Return the maximum expected values for all the answers (no Monte Carlo).

    Parameters
    ----------
    v : ARRAY
        The set of voters.
    c : ARRAY
        The set of candidates.
    vc : ARRAY
        The set of permutations.
    init_distrib : ARRAY
        The initial permutation distribution.

    Returns
    -------
    ev_dict : DICT
        The maximum expected values of the answers (vi,cj>ck).

    """
    # The list of cj > ck.
    comp_cand = np.array(list(permutations(c, 2)))
    # The expected values of the queries.
    ev_array = np.zeros((len(v), len(comp_cand)))

    # Query the i-th voter.
    for i, _ in enumerate(v):
        # Ask the query 'cj > ck ?'.
        for q, _ in enumerate(comp_cand):
            p = proba_query(vc,
                            comp_cand[q][0],
                            comp_cand[q][1],
                            init_distrib,
                            v[i])
            if p > 0:
                # The posterior probability distribution knowing  qi,cj>ck.
                post_distrib = posterior_distrib(vc,
                                                 comp_cand[q][0],
                                                 comp_cand[q][1],
                                                 init_distrib,
                                                 v[i])
                # Borda scores array knowing  qi,cj>ck
                score_cond = list(
                    borda_permut(post_distrib, vc).values())
                # posterior expected value array
                ev_array[i][q] = max(score_cond)
            else:
                ev_array[i][q] = 0

    ev_dict = {'EV(%s,c%s>c%s)' % (v[i], comp_cand[q][0], comp_cand[q][1]):
               ev_array[v[i]][q]
               for i in range(len(v))
               for q in range(len(comp_cand))
               }
    return ev_dict


def expect_value_info_no_mc(v, c, vc, init_distrib, queries):
    """
    Return the expected values of information of the queries (no Monte Carlo).

    Parameters
    ----------
    v : ARRAY
        The set of voters.
    c : ARRAY
        The set of candidates.
    vc : ARRAY
        The set of permutations.
    init_distrib : ARRAY
        The initial permutation distribution.

    Returns
    -------
    evoi_dict : DICT
        The expected values of information EVOI(vi,cj,ck).
    """
    score_init = np.array(list(borda_permut(init_distrib, vc).values()))
    # The expected values of the queries.
    ev_dict = expected_value_no_mc(v, c, vc, init_distrib)
    # Unordered permutations.
    comb = np.array(list(combinations(c, 2)))
    # The expected values of information of all the queries.
    evoi_array = np.zeros((len(v), len(comb)))

    for i, _ in enumerate(v):
        for q, _ in enumerate(comb):
            p_1 = proba_query(vc, comb[q][0], comb[q][1], init_distrib, v[i])
            p_2 = proba_query(vc, comb[q][1], comb[q][0], init_distrib, v[i])
            evoi_array[i][q] = ev_dict[
                'EV(%s,c%s>c%s)'
                % (v[i], comb[q][0], comb[q][1])
                ]*p_1 + ev_dict[
                    'EV(%s,c%s>c%s)'
                    % (v[i], comb[q][1], comb[q][0])
                    ]*p_2

    evoi_array -= max(score_init)
    evoi_dict = {'EVOI(%s,%s,%s)' % (v[i], comb[q][0], comb[q][1]):
                 round(evoi_array[i][q], 4)
                 for i in range(len(v))
                 for q in range(len(comb))
                 if [v[i], comb[q][0], comb[q][1]] not in queries
                 }
    return evoi_dict


def optimal_evoi_query_no_mc(v, c, vc, init_distrib, queries):
    """
    Return the query with the highest EVOI (no Monte Carlo).

    Parameters
    ----------
    v : ARRAY
        The set of voters.
    c : ARRAY
        The set of candidates.
    vc : ARRAY
        The set of permutations.
    init_distrib : ARRAY
        The initial permutation distribution.

    Returns
    -------
    chosen_query : LIST
        The query with the highest EVOI.
    max_chosen_query : FLOAT
        The EVOI of the chosen query.

    """
    evoi_dict = expect_value_info_no_mc(v, c, vc, init_distrib, queries)
    # Choose the query with the highest EVOI.
    max_chosen_query = max(evoi_dict.values())
    print("EVOI of the current query: ", max_chosen_query)
    chosen_query_list = [k for k, v in evoi_dict.items()
                         if v == max_chosen_query]
    # Randomly choose a query among the ones with the highest EVOI.
    chosen_query = [int(s) for s in re.findall(r'\b\d+\b',
                                               rd.choice(chosen_query_list))]
    return(chosen_query, max_chosen_query)
