# -*- coding: utf-8 -*-
"""The Information Gain for Borda heuristic (IGB).

@author: Maeva.Caillat

"""

from itertools import permutations, combinations
import re
import scipy.stats as st
import numpy as np
from numpy import random as rd
from item_winning_proba import win_proba
from other_useful_functions import posterior_distrib, proba_query


# pylint: disable=C0103
def info_gain(v, c, vc, gamma, distrib):
    """
    Return the information gains of all the qi,cj>ck.

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
    distrib : ARRAY
        The current permutation distribution.

    Returns
    -------
    dict
        IG(vi, cj>ck)

    """
    # The list of cj > ck.
    comp_cand = np.array(list(permutations(c, 2)))
    # The information gains of the queries.
    ig_array = np.zeros((len(v), len(comp_cand)))
    # The winning probability array regarding the current distribution.
    pr_win = win_proba(v, c, vc, gamma, distrib)
    # The entropy function.
    entropy = st.entropy(pk=pr_win, base=2)

    # Query the i-th voter.
    for i, _ in enumerate(v):
        # Ask the query 'cj > ck ?'.
        for q, _ in enumerate(comp_cand):
            # The posterior probability distribution knowing  qi,cj>ck.
            post_distrib = posterior_distrib(vc,
                                             comp_cand[q][0],
                                             comp_cand[q][1],
                                             distrib,
                                             v[i])
            # The winning proba array knowing qi,cj>ck.
            post_pr_win = win_proba(v, c, vc, gamma, post_distrib)
            # The posterior entropy function.
            ig_array[i][q] = st.entropy(pk=post_pr_win, base=2)

    ig_array = entropy - ig_array
    ig_dict = {'IG(%s,c%s>c%s)' % (v[i], comp_cand[q][0], comp_cand[q][1]):
               ig_array[v[i]][q]
               for i in range(len(v))
               for q in range(len(comp_cand))
               }
    return ig_dict


def weighted_info_gain(v, c, vc, gamma, distrib, queries):
    """
    Return the weighted information gains of the queries qi,cj,ck.

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
    distrib : ARRAY
        The current permutation distribution.

    Returns
    -------
    dict
        WIG(vi,cj,ck)

    """
    # The information gains of the queries.
    ig_dict = info_gain(v, c, vc, gamma, distrib)
    # Unordered permutations.
    comb = np.array(list(combinations(c, 2)))
    # The weighted information gains of the queries.
    wig_array = np.zeros((len(v), len(comb)))

    for i, _ in enumerate(v):
        for q, _ in enumerate(comb):
            p_1 = proba_query(vc, comb[q][0], comb[q][1], distrib, v[i])
            p_2 = proba_query(vc, comb[q][1], comb[q][0], distrib, v[i])
            # The posterior entropy function.
            wig_array[i][q] = ig_dict[
                'IG(%s,c%s>c%s)'
                % (v[i], comb[q][0], comb[q][1])
                ]*p_1 + ig_dict[
                    'IG(%s,c%s>c%s)'
                    % (v[i], comb[q][1], comb[q][0])
                    ]*p_2

    wig_dict = {'WIG(%s,%s,%s)' % (v[i], comb[q][0], comb[q][1]):
                round(wig_array[i][q], 2)
                for i in range(len(v))
                for q in range(len(comb))
                if [v[i], comb[q][0], comb[q][1]] not in queries
                }
    return wig_dict


def optimal_wig_query(v, c, vc, gamma, distrib, queries):
    """
    Return the query with the highest WIG.

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
    distrib : ARRAY
        The current permutation distribution.


    Returns
    -------
    chosen_query : LIST
        WIG(vi,cj,ck)
    max_chosen_query : FLOAT
        The ingo gain of the chosen query.

    """
    wig_dict = weighted_info_gain(v, c, vc, gamma, distrib, queries)
    # Choose the query with the highest WIG.
    max_chosen_query = max(wig_dict.values())
    print('WIG of the query asked: ', max_chosen_query)
    chosen_query_list = [k for k, v in wig_dict.items()
                         if v == max_chosen_query]
    # Randomly choose a query among the ones with the highest WIG.
    chosen_query = rd.choice(chosen_query_list)
    return([int(s) for s in re.findall(r'\b\d+\b', chosen_query)],
           max_chosen_query)
