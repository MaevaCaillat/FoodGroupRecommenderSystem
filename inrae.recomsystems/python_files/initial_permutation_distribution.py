# -*- coding: utf-8 -*-
"""The initial permutation probability distribution.

@author: Maeva.Caillat

"""

import numpy as np


# pylint: disable=C0103
def init_permut_proba_distrib(vc, rating, v):
    """
    Return an initial permutation probability distribution.

    Parameters
    ----------
    vc : ARRAY
        The set of possible permutations.
    rating : ARRAY
        The rankings of the candidates by the users.
    v : ARRAY
        The set of voters.

    Returns
    -------
    init_distrib : ARRAY
        The initial permutation distribution.

    """
    # The array of appearances of each permutation in the training set.
    app = np.zeros(len(vc))

    for i, _ in enumerate(rating):
        j = 0
        while (j <= len(vc) and not np.all(rating[i] == vc[j])):
            j += 1
        app[j] += 1

    # we use Laplace's principle
    app += 1
    app /= sum(app)
    init_distrib = np.tile(app, (len(v), 1))
    return init_distrib
