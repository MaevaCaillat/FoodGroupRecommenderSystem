# -*- coding: utf-8 -*-
"""The highest expected score heuristic for Borda (ESB).

@author: Maeva.Caillat

This module implements the ESB heuristic.

"""

from itertools import permutations, combinations
import re
import numpy as np
from numpy import random as rd
from item_winning_proba import win_proba
from other_useful_functions import posterior_distrib, proba_query


# pylint: disable=C0103
def expected_max(v, c, vc, gamma, init_distrib):
    """
    Return the expected maximum of qi,cj>ck.

    Parameters
    ----------
    v : ARRAY
        The set of voters.
    c : ARRAY
        The set of candidates.
    vc : ARRAY
        The set of permutations.
    gamma : INT
        The sample size.
    init_distrib : ARRAY
        The initial permutation distribution.

    Returns
    -------
    em_dict : DICT
        EM(vi,cj>ck)

    """
    # The list of cj > ck.
    comp_cand = np.array(list(permutations(c, 2)))
    # The expected maximums of the queries.
    em_array = np.zeros((len(v), len(comp_cand)))
    # Winning proba of the current state
    pr_win = win_proba(v, c, vc, gamma, init_distrib)

    # Query the i-th voter.
    for i, _ in enumerate(v):
        # Ask the query 'cj > ck ?'.
        for q, _ in enumerate(comp_cand):
            # The posterior probability distributions knowing  qi,cj>ck.
            post_distrib = posterior_distrib(vc,
                                             comp_cand[q][0],
                                             comp_cand[q][1],
                                             init_distrib,
                                             v[i])
            # The winning proba array knowing  qi,cj>ck.
            post_pr_win = win_proba(v, c, vc, gamma, post_distrib)
            # The posterior entropy function.
            em_array[i][q] = max(post_pr_win)

    em_array = em_array - max(pr_win)
    em_dict = {'EM(%s,c%s>c%s)' % (v[i], comp_cand[q][0], comp_cand[q][1]):
               em_array[i][q]
               for i in range(len(v))
               for q in range(len(comp_cand))
               }
    return em_dict


def weighted_expect_max(v, c, vc, gamma, init_distrib, queries):
    """
    Return the weighted expected maximum of qi,cj,ck.

    Parameters
    ----------
    v : ARRAY
        The set of voters.
    c : ARRAY
        The set of candidates.
    vc : ARRAY
        The set of permutations.
    gamma : INT
        The sample size.
    init_distrib : ARRAY
        The initial permutation distribution.

    Returns
    -------
    wem_dict : DICT
        WEM(vi,cj,ck)

    """
    # The information gains of the queries.
    em_dict = expected_max(v, c, vc, gamma, init_distrib)
    # Unordered permutations.
    comb = np.array(list(combinations(c, 2)))
    # The weighted information gains of the queries.
    wem_array = np.zeros((len(v), len(comb)))

    for i, _ in enumerate(v):
        for q, _ in enumerate(comb):
            p_1 = proba_query(vc, comb[q][0], comb[q][1], init_distrib, v[i])
            p_2 = proba_query(vc, comb[q][1], comb[q][0], init_distrib, v[i])
            # The posterior entropy function.
            wem_array[i][q] = em_dict[
                'EM(%s,c%s>c%s)'
                % (v[i], comb[q][0], comb[q][1])
                ]*p_1 + em_dict[
                    'EM(%s,c%s>c%s)'
                    % (v[i], comb[q][1], comb[q][0])
                    ]*p_2
    wem_dict = {'WEM(%s,%s,%s)' % (v[i], comb[q][0], comb[q][1]):
                round(wem_array[i][q], 2)
                for i in range(len(v))
                for q in range(len(comb))
                if [v[i], comb[q][0], comb[q][1]] not in queries
                }
    return wem_dict


def optimal_wem_query(v, c, vc, gamma, init_distrib, queries):
    """
    Return the query with the highest WEM.

    Parameters
    ----------
    v : ARRAY
        The set of voters.
    c : ARRAY
        The set of candidates.
    vc : ARRAY
        The set of permutations.
    gamma : INT
        The sample size.
    init_distrib : ARRAY
        The initial permutation distribution.

    Returns
    -------
    chosen_query : LIST
        WEM(vi,cj,ck)
    max_chosen_query : FLOAT
        The WEM of the chosen query.

    """
    wem_dict = weighted_expect_max(v, c, vc, gamma, init_distrib, queries)
    # Choose the query with the highest EVOI.
    max_chosen_query = max(wem_dict.values())
    print('WEM of the query asked: ', max_chosen_query)
    # Randomly choose a query among the ones with the highest WIG
    chosen_query = rd.choice([k for k, v in wem_dict.items()
                              if v == max_chosen_query])
    return([int(s) for s in re.findall(r'\b\d+\b', chosen_query)],
           max_chosen_query)
