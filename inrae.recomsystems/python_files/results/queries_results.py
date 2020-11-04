# -*- coding: utf-8 -*-
"""The number of queries results and graphs associated.

Created on Fri Sep 4 2020

@author: Maeva.Caillat

"""

import numpy as np
from matplotlib import pyplot as plt


# pylint: disable=C0103
dataset = np.array([5, 7, 10, 12, 15])
igb_query = np.array(
    [37.64,
     48.48,
     65.32,
     94.96,
     123.64]
    )
igb_var = np.array(
    [24.6304,
     53.8496,
     150.4576,
     215.1584,
     232.7904]
    )
esb_query = np.array(
    [40.16,
     51.24,
     71.08,
     109.52,
     128.08
     ]
    )
esb_var = np.array(
    [45.3344,
     58.2624,
     69.5136,
     122.2496,
     162.8736
     ]
    )
evoi_query = np.array(
    [39.92,
     49.56,
     69.08,
     99.2,
     119.44]
    )
evoi_var = np.array(
    [22.2336,
     64.0864,
     76.4736,
     202.8,
     192.7264]
    )
evoi_igb_query = np.array(
    [38.44,
     47.12,
     64.36,
     90.04,
     120.4]
    )
evoi_igb_var = np.array(
    [20.2464,
     47.0656,
     109.1904,
     244.4384,
     338.16
     ]
    )
fig, ax = plt.subplots()
plt.errorbar(dataset, igb_query,
             np.sqrt(igb_var),
             elinewidth=1,
             linestyle='-',
             color='r',
             marker='s',
             label='IGB')
plt.errorbar(dataset, esb_query,
             np.sqrt(esb_var),
             elinewidth=1,
             linestyle='-',
             color='b',
             marker='d',
             label='ESB')
plt.errorbar(dataset, evoi_query,
             np.sqrt(evoi_var),
             elinewidth=1,
             linestyle='-',
             color='purple',
             marker='^',
             label='EVOI')
plt.errorbar(dataset, evoi_igb_query,
             np.sqrt(evoi_igb_var),
             elinewidth=1,
             linestyle='-',
             color='green',
             marker='o',
             label='EVOI+IGB')
ax.legend()
ax.set_xlim(4, 16)
ax.set_ylim(30, 145)
plt.title('Queries on the sushi dataset')
plt.xlabel('dataset (users x items)')
plt.xticks(dataset, ['%s x %s' % (int(i), 6)
                     for i in dataset])
plt.ylabel('number of queries')
plt.show()
