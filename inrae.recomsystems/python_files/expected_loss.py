# -*- coding: utf-8 -*-
"""The Expected Loss.

@author: Maeva.Caillat

This module contains a function computing the expected loss.

"""

import numpy as np
from numpy import random as rd
from borda_voting_protocol import borda, borda_permut


# pylint: disable=C0103
def expected_loss(v, c, vc, n, distrib):
    """
    Return the expected loss estimated with Monte Carlo.

    Parameters
    ----------
    v : ARRAY
        The set of voters.
    c : ARRAY
        The set of candidates.
    vc : ARRAY
        The set of permutations.
    n : INT
        The sample size for the expected loss (Monte Carlo).
    distrib : ARRAY
        The current permutation distribution.

    Returns
    -------
    expect_loss : INT
        The expected loss estimated with Monte Carlo.

    """
    # Initialize the expected Borda scores.
    eu_array = np.array(list(borda_permut(distrib, vc).values()))
    # The candidate with the highest expected Borda score.
    winner = np.argmax(eu_array)
    expect_loss = 0
    # Loop on the samples.
    for _ in range(n):
        rd_permut = []
        # For voter i, sample a permutation from vci.
        for i in range(len(v)):
            # Choose a permutation using the probabilities associated.
            rd_permut.append(vc[rd.choice(len(vc), 1, p=distrib[i])])
        all_rd_permut = np.array(rd_permut).flatten().reshape((len(v), len(c)))
        # Find the local scores using the Borda voting protocol.
        local_scores = np.array(list(borda(all_rd_permut).values()))
        # Compute the local expected loss.
        local_loss = max(local_scores) - local_scores[winner]
        # Add the local expected loss to the previous expected losses.
        expect_loss += local_loss
    # Divide the accumulated Borda scores by the sample size.
    expect_loss /= n
    return expect_loss
