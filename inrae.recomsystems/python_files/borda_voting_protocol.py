# -*- coding: utf-8 -*-
"""The Borda Voting protocol.

@author: Maeva.Caillat

This module contains 2 functions computing borda scores,
from ratings or distributions.

"""

import numpy as np


# pylint: disable=C0103
def borda(rating):
    """
    Return the Borda scores of the candidates according to their rankings.

    Parameters
    ----------
    rating : ARRAY
        The rankings of the candidates by the users.

    Returns
    -------
    stats : DICT
        The borda scores of the candidates.

    """
    # The maximal number of points equals to nb_candidates - 1.
    max_points = len(rating[0]) - 1
    count_points = np.zeros(len(rating[0]))

    for i in range(len(rating)):
        for j in range(len(rating[0])):
            # The preferred item receives max_points,
            # the second-preferred max_points-1...
            count_points[int(rating[i, j])] += max_points - j

    stats = {str(k): count_points[k] for k in range(len(count_points))}
    return stats


def borda_permut(distrib, vc):
    """
    Return the expected Borda scores regarding distrib.

    Parameters
    ----------
    distrib : ARRAY
        The current permutation distribution.
    vc : ARRAY
        The set of permutations.

    Returns
    -------
    stats : DICT
        The expected borda scores of the candidates.

    """
    # The maximal number of points equals to nb_candidates - 1.
    max_points = len(vc[0]) - 1
    count_points = np.zeros(len(vc[0]))

    for i in range(len(vc)):
        for j in range(len(vc[0])):
            # The preferred item receives max_points*P(permutation),
            # the second-preferred (max_points-1)*P(permutation)...
            count_points[
                int(vc[i, j])
                ] += (max_points-j) * sum(distrib[:, i])

    stats = {str(r): count_points[r] for r in range(len(count_points))}
    return stats


def borda_missing(rating):
    """
    Return the Borda scores of the candidates according to their rankings.
    Candidates can be excluded by voters (penalty).

    Parameters
    ----------
    rating : ARRAY
        The rankings of the candidates by the users.

    Returns
    -------
    stats : DICT
        The borda scores of the candidates.

    """
    # The maximal number of points equals to nb_candidates - 1.
    max_points = len(rating[0]) - 1
    count_points = np.zeros(len(rating[0]))
    candidate = np.arange(5)
    for i in range(len(rating)):
        j = 0
        while (j < 5) and isinstance(rating[i, j], int):
            count_points[int(rating[i, j])] += max_points - j
            j += 1
        inters = [e for e in candidate if e not in rating[i]]
        count_points[inters] -= 2

    stats = {str(k): count_points[k] for k in range(len(count_points))}
    return stats
