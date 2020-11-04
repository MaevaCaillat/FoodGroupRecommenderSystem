# -*- coding: utf-8 -*-
"""Some useful functions.

@author: Maeva.Caillat

This module contains some useful functons to:
    - calculate a posterior distribution knowing a preference,
    - calculate the proba of a preference,
    - determinate the answer of a query,
    - apply transitivity at every query.

"""

import numpy as np


# pylint: disable=C0103
def index_query(vc, cj, ck):
    """
    Return the indexes in the permutations array corresponding to  cj > ck.

    Parameters
    ----------
    vc : ARRAY
        The set of voters.
    cj : INT
        Candidate j.
    ck : INT
        Candidate k.

    Returns.
    -------
    index_cj_ck : LIST
        The list of indexes in the permut array for cj > ck.

    """
    index_cj_ck = []
    index_ck_cj = []
    for e, _ in enumerate(vc):
        if vc[e][0] == cj:
            index_cj_ck.append(e)
        elif vc[e][0] == ck:
            index_ck_cj.append(e)
        else:
            jcj = 0
            jck = 0
            j = 1
            while (jcj == 0 or
                   jck == 0):
                if vc[e][j] == cj:
                    jcj = j
                elif vc[e][j] == ck:
                    jck = j
                j += 1
            if jcj < jck:
                index_cj_ck.append(e)
            else:
                index_ck_cj.append(e)
    return index_cj_ck


def posterior_distrib(vc, cj, ck, init_distrib, vi):
    """
    Return the posterior probability distributions knowing qi, cj>ck.

    Parameters
    ----------
    vc : ARRAY
        The set of possible permutations.
    cj : INT
        Candidate j.
    ck : INT
        Candidate k.
    init_distrib : ARRAY
        The initial permutation distribution.
    vi : INT
        Voter i.

    Returns
    -------
    distrib : ARRAY
        The posterior distrib knowing qi, cj>ck.

    """
    distrib = np.copy(init_distrib)
    index_cj_ck = index_query(vc, cj, ck)

    s = sum(distrib[vi][index_cj_ck])
    if s != 0:
        p = 1/s
        for r in range(len(distrib[vi])):
            if r in index_cj_ck:
                distrib[vi][r] *= p
            else:
                distrib[vi][r] = 0
    return distrib


def proba_query(vc, cj, ck, distrib, vi):
    """
    Return the probability of the query qi,cj>ck.

    Parameters
    ----------
    vc : ARRAY
        The set of possible permutations.
    cj : INTarray
        Candidate j.
    ck : INT
        Candidate k.
    distrib : ARRAY
        The current permutation distribution.
    vi : INT
        Voter i.

    Returns
    -------
    p : FLOAT
        The proba of qi,cj>ck.

    """
    index_cj_ck = index_query(vc, cj, ck)
    p = sum(distrib[vi][index_cj_ck])
    return p


def deterministic_answers_to_query(vi, cj, ck, rating):
    """
    Return 1 if vi prefers cj to ck and 0 otherwise.

    Parameters
    ----------
    vi : INT
        Voter i.
    cj : INT
        Candidate j.
    ck : INT
        Candidate k.
    rating : ARRAY
        The rankings of the candidates by the users.

    Returns
    -------
    int
        0 or 1.

    """
    j = 0
    k = 0
    while rating[vi][j] != cj:
        j += 1
    while rating[vi][k] != ck:
        k += 1
    if j < k:
        return 1
    return 0


def transitivity_complete(answer,
                          vi,
                          cj,
                          ck,
                          p_min,
                          p_max,
                          vc,
                          distrib,
                          queries,
                          list_alternative_worst):
    """
    Use the transitivity of preferences.

    Parameters
    ----------
    answer : INT
        1 if cj>ck, 0 otherwise.
    vi : INT
        The ith user.
    cj : INT
        The jth candidate.
    ck : INT
        The kth candidate.
    p_min : ARRAY
        The possible minima array.
    p_max : ARRAY
        The possible maxima array.
    vc : ARRAY
        The set of permutations.
    distrib : ARRAY
        The permutation distribution.
    queries : ARRAY
        The answers already known.
    list_alternative_worst : LIST OF LISTS
        One list per user, in each one list per candidate
        containing the candidates inferior to this very candidate.

    Returns
    -------
    p_min : ARRAY
        The possible minimma array updated.
    p_max : ARRAY
        The possible maxima array updated.
    distrib : ARRAY
        The permutation distribution updated.
    queries : ARRAY
        The list of answers updated.
    list_alternative_worst : LIST of LISTS
        The list of inferior candidates for every candidate
        and every user updated.

    """
    # If cj is preferred to ck.
    if int(answer) == 1:
        c_best = cj
        c_worst = ck
    # If ck is preferred to cj.
    else:
        c_best = ck
        c_worst = cj

    print("User v" + str(vi)
          + " prefers c" + str(c_best)
          + " to c" + str(c_worst) + ".")

    # Update the rankings distribution regarding this answer.
    distrib = posterior_distrib(vc, c_best, c_worst, distrib, vi)

    # Add c_worst to the list of inferior candidates of c_best for vi.
    list_alternative_worst[vi][c_best].append(c_worst)
    # The possible min of c_best increases of 1.
    p_min[c_best] += 1
    # The possible max of c_worst decreases of 1.
    p_max[c_worst] -= 1

    # Loop on the list of inferior items of c_worst for vi.
    for alt in list_alternative_worst[vi][c_worst]:
        # If c_worst>alt and alt not compared to c_best yet, add c_best>alt.
        if alt not in list_alternative_worst[vi][c_best]:
            list_alternative_worst[vi][c_best].append(alt)
            p_min[c_best] += 1
            p_max[alt] -= 1
            queries.append([vi, min(alt, c_best), max(alt, c_best)])
    for a in range(len(list_alternative_worst[vi])):
        # If a>c_best for vi, c_worst not compared to a yet, add a>c_worst.
        if (c_best in list_alternative_worst[vi][a] and
                c_worst not in list_alternative_worst[vi][a]):
            p_min[a] += 1
            p_max[c_worst] -= 1
            queries.append([vi, min(a,
                                    c_worst),
                            max(a,
                                c_worst)])
            list_alternative_worst[vi][a].append(c_worst)
    return(p_min,
           p_max,
           distrib,
           queries,
           list_alternative_worst)
