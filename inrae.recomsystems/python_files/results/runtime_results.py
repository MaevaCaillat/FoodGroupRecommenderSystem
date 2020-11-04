# -*- coding: utf-8 -*-
"""The runtimes per query results and graphs associated.

Created on Fri Sep 4 2020

@author: Maeva.Caillat

"""

import numpy as np
from matplotlib import pyplot as plt


# pylint: disable=C0103
dataset = np.array([5, 7, 10, 12, 15])
igb_runtime = np.array(
    [16.21001579,
     30.3116552,
     59.038739,
     83.93924043,
     128.90869051]
    )
esb_runtime = np.array(
    [16.48795539,
     30.21143464,
     59.3504147,
     84.17453342,
     129.07287036]
    )
evoi_runtime = np.array(
    [2.92486122,
     4.67078116,
     6.75214057,
     8.2089384,
     10.9774342]
    )
evoi_igb_runtime = np.array(
    [16.27866312,
     32.81606864,
     64.78881187,
     87.30603623,
     137.66562152
     ]
    )
fig, ax = plt.subplots()
ax.plot(dataset, igb_runtime,
        linestyle='-',
        color='r',
        marker='s',
        label='IGB')
ax.plot(dataset, esb_runtime,
        linestyle='-',
        color='b',
        marker='d',
        label='ESB')
ax.plot(dataset, evoi_runtime,
        linestyle='-',
        color='purple',
        marker='^',
        label='EVOI')
ax.plot(dataset, evoi_igb_runtime,
        linestyle='-',
        color='green',
        marker='o',
        label='EVOI+IGB')
ax.legend()
ax.set_xlim(4, 16)
ax.set_ylim(0, 150)
plt.title('Runtime on the sushi dataset')
plt.xlabel('dataset (users x items)')
plt.xticks(dataset, ['%s x %s' % (int(i), 6)
                     for i in dataset])
plt.ylabel('runtime per query (seconds)')
plt.show()
# -*- coding: utf-8 -*-
