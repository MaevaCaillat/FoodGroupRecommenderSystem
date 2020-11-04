#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generating rankings from datasets.

Created on Wed Jul  1 10:57:58 2020

@author: Maeva.Caillat

This module generates rankings for the sushi and the random datasets.
"""
from itertools import permutations
from math import factorial
import pandas as pd
import numpy as np
from numpy import random as rd
from initial_permutation_distribution import init_permut_proba_distrib


# pylint: disable=C0103
def random_dataset_sushi(nb_user,
                         nb_item,
                         nb_matrix,
                         nb_user_init_distrib,
                         file_path):
    """
    Return 5000 rankings on 6 sushis and an initial permutation distribution.

    Parameters
    ----------
    nb_user : INT
        The number of users.
    nb_item : INT
        The number of items.
    nb_matrix : INT
        The number of matrices needed for generating
        an initial permutation distribution for the sushi dataset.
    nb_user_init_distrib : INT
        The number of users needed for generating
        an initial permutation distribution for the sushi dataset.

    Returns
    -------
    list_some_sushi_ranking : LIST
        The list of 5000 rankings on 6 sushis.
    distrib : ARRAY
        The initial permutation distribution for the sushi dataset.

    """
    # We gather the 5000 rankings of 10 sushis.
    list_sushi_ranking = (pd.read_csv(
        file_path,
        sep=' ',
        header=None,
        skiprows=1,
        usecols=list(range(2, 12)))).values.tolist()

    # We only keep sushis 0 to 5 to compare with the Israeli paper.
    list_some_sushi_ranking = []
    for i, _ in enumerate(list_sushi_ranking):
        list_some_sushi_ranking.append(
            list(
                filter(
                    lambda x: x not in [6, 7, 8, 9],
                    list_sushi_ranking[i])))

    # Indexes of random lines for the first lines of random matrices
    # that serve to initiate a permutation distribution.
    index_lines_rd_matrices = rd.choice(
        len(list_some_sushi_ranking) - nb_user_init_distrib,
        nb_matrix)

    # We extract nb_matrix blocks of size nb_user_init_distrib
    # in the original ranking list.
    last_ranking_list = []
    for j in index_lines_rd_matrices:
        for k in range(nb_user_init_distrib):
            last_ranking_list.append(list_some_sushi_ranking[j+k])

    # New id for the users extracted for initiating a distribution.
    # The set of voters.
    v_init_distrib = (np.array(
        range(pd.DataFrame(last_ranking_list).shape[0]))).flatten()
    # The set of possible permutations.
    vc = np.array(list(permutations(np.arange(len(last_ranking_list[0])))))
    # The initial distribution for the wanted number of voters.
    distrib = np.tile(init_permut_proba_distrib(vc,
                                                np.array(last_ranking_list),
                                                v_init_distrib)[0],
                      nb_user).reshape(nb_user, factorial(nb_item))

    # Indexes of random lines for random matrices.
    index_lines = rd.choice(
        len(list_some_sushi_ranking)-nb_user, 1)
    # Array of ratings. Lines: users. Columns: rankings.
    # First item in the line: preferred item.
    ranking_list = []
    for j in index_lines:
        # We consider blocks of size nb_matrix in the ranking list.
        for u in range(nb_user):
            ranking_list.append(list_some_sushi_ranking[j+u])

    df_rating = pd.DataFrame(ranking_list)
    return(df_rating, distrib)


def fixed_dataset_sushi(nb_user,
                        nb_item,
                        nb_matrix,
                        nb_user_init_distrib,
                        file_path):
    """
    Return 5000 rankings on 6 sushis and an initial permutation distribution.

    Parameters
    ----------
    nb_user : INT
        The number of users.
    nb_item : INT
        The number of items.
    nb_matrix : INT
        The number of matrices needed for generating
        an initial permutation distribution for the sushi dataset.
    nb_user_init_distrib : INT
        The number of users needed for generating
        an initial permutation distribution for the sushi dataset.

    Returns
    -------
    list_some_sushi_ranking : LIST
        The list of 5000 rankings on 6 sushis.
    distrib : ARRAY
        The initial permutation distribution for the sushi dataset.

    """
    # We gather the 5000 rankings of 10 sushis.
    list_sushi_ranking = (pd.read_csv(
        file_path,
        sep=' ',
        header=None,
        skiprows=1,
        usecols=list(range(2, 12)))).values.tolist()

    # We only keep sushis 0 to 5 to compare with the Israeli paper.
    list_some_sushi_ranking = []
    for i, _ in enumerate(list_sushi_ranking):
        list_some_sushi_ranking.append(
            list(
                filter(
                    lambda x: x not in [6, 7, 8, 9],
                    list_sushi_ranking[i])))

    # We extract nb_matrix blocks of size nb_user_init_distrib
    # in the original ranking list.
    last_ranking_list = list_some_sushi_ranking[:nb_matrix*nb_user_init_distrib]

    # New id for the users extracted for initiating a distribution.
    # The set of voters.
    v_init_distrib = (np.array(
        range(pd.DataFrame(last_ranking_list).shape[0]))).flatten()
    # The set of possible permutations.
    vc = np.array(list(permutations(np.arange(len(last_ranking_list[0])))))
    # The initial distribution for the wanted number of voters.
    distrib = np.tile(init_permut_proba_distrib(vc,
                                                np.array(last_ranking_list),
                                                v_init_distrib)[0],
                      nb_user).reshape(nb_user, factorial(nb_item))

    # Array of ratings. Lines: users. Columns: rankings.
    # First item in the line: preferred item.
    ranking_list = list_some_sushi_ranking[:nb_user]

    df_rating = pd.DataFrame(ranking_list)
    return(df_rating, distrib)


def dataset_random(nb_user, nb_item):
    """
    Return nb_user random rankings on nb_item and init_distrib.

    Parameters
    ----------
    nb_user : INT
        Number of users.
    nb_item : INT
        Number of items.

    Returns
    -------
    df_rating : DATAFRAME
        nb_user random rankings on nb_item.
    init_distrib : ARRAY
        The initial permutation distribution.

    """
    # Array of ratings. Lines: users. Columns: rankings.
    # First item in the line: preferred item.
    df = rd.permutation(nb_item)
    for _ in range(nb_user-1):
        df = np.append(df, rd.permutation(nb_item))
    df_rating = pd.DataFrame(df.reshape(nb_user, nb_item))
    # Id of the users.
    df_user_id = pd.DataFrame(np.array(range(df_rating.shape[0])))
    # The set of voters.
    v = np.array(df_user_id).flatten()
    # The rankings of the candidates by the users.
    rating = np.array(df_rating)
    # The set of candidate items.
    c = np.arange(len(rating[0]))
    # The set of possible permutations .
    vc = np.array(list(permutations(c)))
    # The initial distribution.
    init_distrib = init_permut_proba_distrib(vc, rating, v)

    return(df_rating, init_distrib)


def nutrition_dataset(file_path):
    """
    Return 130 rankings on 5 starters, 5 dishes, 5 desserts.

    Parameters
    ----------
    file_path : STRING
        The file path to the CROUS dataset.

    Returns
    -------
    starter_ranking: DATAFRAME
        The dataframe containing the 130 rankings over 5 starters.
    main_ranking: DATAFRAME
        The dataframe containing the 130 rankings over 5 main dishes.
    dessert_ranking: DATAFRAME
        The dataframe containing the 130 rankings over 5 desserts.
    """
    starter_ranking = pd.DataFrame((pd.read_excel(
        file_path,
        header=None,
        skiprows=1,
        sheet_name='starters',
        keep_default_na=False,
        usecols=list(range(1, 6)))).values.tolist())

    main_ranking = pd.DataFrame((pd.read_excel(
        file_path,
        header=None,
        skiprows=1,
        sheet_name='main courses',
        keep_default_na=False,
        usecols=list(range(1, 6)))).values.tolist())

    dessert_ranking = pd.DataFrame((pd.read_excel(
        file_path,
        header=None,
        skiprows=1,
        sheet_name='desserts',
        keep_default_na=False,
        usecols=list(range(1, 6)))).values.tolist())

    return(np.array(starter_ranking), np.array(main_ranking),
           np.array(dessert_ranking))
