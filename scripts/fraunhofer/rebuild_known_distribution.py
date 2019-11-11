# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright 2019 by ShabaniPy Authors, see AUTHORS for more details.
#
# Distributed under the terms of the MIT license.
#
# The full license is in the file LICENCE, distributed with this software.
# -----------------------------------------------------------------------------
"""Rebuild a known current distribution.

"""
from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt
from dynesty import plotting as dyplot

from shabanipy.fraunhofer.estimation import rebuild_current_distribution
from shabanipy.fraunhofer.util import produce_fraunhofer

# Current and phase distribution to use.
DISTRIBUTIONS = [
    ([1, 1, 1, 1, 1], [0, 0, 0, 0, 0]),
    ([2.5, 0, 0, 0, 2.5], [0, 0, 0, 0, np.pi/4])
]


for d, p in DISTRIBUTIONS:
    b = np.linspace(-5, 5, 101)
    f = produce_fraunhofer(b, np.pi/4, 4, d, p)
    a = f[50]
    f[50] = f[51]
    f[51] = a
    plt.plot(b, f)
    plt.show()

    res = rebuild_current_distribution(b, f, 4, 5)

    params = res["fraunhofer_params"]
    plt.plot(b, f)
    plt.plot(b,
             params["amplitude"] *
             produce_fraunhofer(b-params["offset"], params["field_to_k"], 4, d, p)
             )

    fig, axes = dyplot.traceplot(res)
    fig.tight_layout()
    plt.show()
