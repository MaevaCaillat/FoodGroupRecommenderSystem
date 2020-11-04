# -*- coding: utf-8 -*-
"""Computing the winning probabilities of the candidates.

@author: Maeva.Caillat

"""

import operator
import numpy as np
from numpy import random as rd
from borda_voting_protocol import borda


# pylint: disable=C0103
def win_proba(v, c, vc, gamma, distrib):
    """
    Return the estimated winning probabilities of the candidates.

    Parameters
    ----------
    v : ARRAY
        The set of voters.
    c : ARRAY
        The set of candidate items.
    vc : ARRAY
        The set of possible permutations.
    gamma : INT
        The sample size.
    distrib : ARRAY
        The current rankings probability distributions.

    Returns an array.
    -------
    pr_win : ARRAY
        The winning proba array.

    """
    # Initialize.
    pr_win = np.zeros(len(c))
    # Loop on the sample size.
    for _ in range(gamma):
        rd_permut = []
        # Loop on the number of voters.
        for i in range(len(v)):
            # Draw a permutation for voter i regarding distrib[i].
            rd_permut.append(vc[rd.choice(len(vc), 1, p=distrib[i])])
        all_rd_permut = np.array(rd_permut).flatten().reshape((len(v), len(c)))

        # Compute the items expected Borda scores regarding the drawn rankings.
        local_borda_scores = borda(all_rd_permut)
        # The local winner is the item with the highest expected Borda score.
        local_winner = int(max(local_borda_scores.items(),
                               key=operator.itemgetter(1))[0])
        # Add 1 to the local winning candidate.
        pr_win[local_winner] += 1

    # Divide the number of times the items won by the number of iterations.
    pr_win /= gamma
    # Return the winning probabilities array.
    return pr_win
