# -*- coding: utf-8 -*-
"""The variables.

@author: Maeva.Caillat

This module contains the variables needed to test the code.

"""


# pylint: disable=C0103
nb_user = 5
"""int: The number of users.

In the Israeli paper, nb_user is worth 5 to 25.
"""

nb_item = 6
"""int: The number of items.

In the Israeli paper, nb_items represents 5 movies or 6 sushis.
"""

gamma = 300
"""int: The sample size for PrWin and the Expected Utility.

In the Israeli paper, gamma = 300.
"""

epsilon = 0.15
"""float: The desired threeshold for the expected utility loss.

It represents the probability of making an error
on the expected loss higher than epsilon.
"""

delta = 0.05
"""float: The confidence parameter.

It is often worth 1-95% or 1-99%.
"""

termination_value = 0
"""float: The termination value for the expected loss.

Ideally, 0.
"""

heuristic = 'EVOI'
"""string: The name of the heuristic.

It could be IGB, ESB, EVOI or EVOI+IGB.
"""

nb_experiment = 1
"""string: The number of times each experiment is run.

It is necessary to accommodate for randomness, since IGB and ESB use sampling.
In the Israeli paper, 25 times.
"""

database = 'fixed_sushi'
"""string: The name of the dataset used.

It can be random or fixed_sushi or random_sushi.
"""

nb_matrix = 10
"""int: The number of matrices for generating a permutation distribution.

It is used for the sushi dataset, and it is worth 10 in the Israeli paper.
"""

nb_user_init_distrib = 10
"""int: The number of users for generating a permutation distribution.

It is used for the sushi dataset, and it is worth 10 in the Israeli paper.
"""

israeli = False
"""bool: True to use the Israeli methods, False to use the expected loss too.
"""

"""MY_PATH_SUSHI = ('/home/mmip/Documents/Python/prefelicitgroup/'
                 + 'inrae.recomsystems/inrae.recomsystems/data/'
                 + 'sushi3a.5000.10.order')"""
"""MY_PATH_SUSHI = ('/Users/sonialementec/Documents/INRAE/Git/'
                 + 'inrae.recomsystems/inrae.recomsystems/data/'
                 + 'sushi3a.5000.10.order')"""
MY_PATH_SUSHI = ('C:/Users/maeva/Documents/Cours_ei4/INRAE/prefelicitgroup/'
                 + 'inrae.recomsystems/inrae.recomsystems/data/'
                 + 'sushi3a.5000.10.order')
"""string: The path on the computer where the database sushi is stored.

"""

CROUS_PATH = ('/home/mmip/Documents/Python/prefelicitgroup/'
              + 'inrae.recomsystems/inrae.recomsystems/data/'
              + 'crous.130.5.order.xlsx')
"""string: The path on the computer where the crous database is stored.

"""
