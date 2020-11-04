# -*- coding: utf-8 -*-
"""The communication cut results and graphs associated.

Created on Fri Sep 4 2020

@author: Maeva.Caillat

"""

import numpy as np
from matplotlib import pyplot as plt


# pylint: disable=C0103
dataset = np.array([5, 7, 10, 12, 15])
igb_queried = np.array(
    [49.81333333,
     53.82857143,
     56.45333333,
     47.24444444,
     45.04888889]
    )
esb_queried = np.array(
    [46.45333333,
     51.2,
     52.61333333,
     39.15555556,
     43.07555556]
    )
evoi_queried = np.array(
    [46.77333333,
     52.8,
     53.94666667,
     44.88888889,
     46.91555556]
    )
evoi_igb_queried = np.array(
    [48.74666667,
     55.12380952,
     57.09333333,
     49.97777778,
     46.48888889]
    )
fig, ax = plt.subplots()
ax.plot(dataset, igb_queried,
        linestyle='-',
        color='r',
        marker='s',
        label='IGB')
ax.plot(dataset, esb_queried,
        linestyle='-',
        color='b',
        marker='d',
        label='ESB')
ax.plot(dataset, evoi_queried,
        linestyle='-',
        color='purple',
        marker='^',
        label='EVOI')
ax.plot(dataset, evoi_igb_queried,
        linestyle='-',
        color='green',
        marker='o',
        label='EVOI+IGB')
ax.legend()
ax.set_xlim(4, 16)
ax.set_ylim(30, 65)
plt.title('Communication performance on the sushi dataset')
plt.xlabel('dataset (users x items)')
plt.xticks(dataset, ['%s x %s' % (int(i), 6)
                     for i in dataset])
plt.ylabel('cut in the communication (%)')
plt.show()
