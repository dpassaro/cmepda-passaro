"""
Assingnment 2: ProbabilityDensityFunction class
"""

import logging

import numpy as np
import matplotlib.pylab as plt
from scipy.interpolate import InterpolatedUnivariateSpline

#--------------------------------------------------------------

def inv_cumulative_func(y_value, spline, x_min, x_max):
    """ Compute the cumulative function of a pdf
    """
    norm = spline.integral(x_min, x_max)
    x_axis = np.linspace(x_min, x_max, 100)
    y_axis = np.array( [ spline.integral(x_min, value)/norm \
                        for value in x_axis ] )

    inv_func = InterpolatedUnivariateSpline(y_axis, x_axis, k=3)
    return inv_func(y_value)

#--------------------------------------------------------------

class ProbDensFunc:
    """ Class to handle the propability density function of
        a variable (x), given its distribution (y). This class
        then throws random numbers according to the pdf.
    """

    def __init__(self, x, y, order = 3):
        """ Constructor; creates a spline of a givien order (3 default)
            based on (x,y) distribution
        """
        self._x = np.array(x)
        self._y = np.array(y)
        self._min = np.amin(self._x)
        self._max = np.amax(self._x)
        if x.size != y.size :
            logging.error("x and y arrays must have same lenght")
        if np.any(y<0) :
            logging.error("y must be non-negative")
        self._order = order
        self._spline = InterpolatedUnivariateSpline(x, y, k = order)

    def __call__(self, x_value):
        """ call method """
        if x_value < self._min or x_value > self._max:
            logging.error("x out of dominium of definition")
        return self._spline(x_value)

    def compute_probability(self, x_min, x_max):
        """ Method to compute the probability for x in [x_min, x_max]
        """
        norm = self._spline.integral(self._min, self._max)

        if x_min<x_max:
            return self._spline.integral(x_min, x_max)/norm
        return self._spline.integral(x_max, x_min)/norm

    def random(self, number = 1):
        """ Method to throw random number according to the pdf
        """
        random_value = np.random.random(size = number)
        pdf_random = np.array([ inv_cumulative_func(el, self._spline, \
                            self._min, self._max) for el in random_value])
        return pdf_random

#--------------------------------------------------------------

if __name__ == "__main__":

    N = 10000
    x_array = np.linspace(0.,5., N)
    y_array = np.exp(-1.*x_array)
    pdf = ProbDensFunc(x_array, y_array, order=3)
    random_array = pdf.random(N)
    n, bins, patches = plt.hist(x=random_array, bins='auto', color='#0504aa',
                                alpha=0.7, rwidth=0.85, density=True)
    plt.grid(alpha = 0.75)
    plt.xlabel('x value')
    plt.ylabel('occurences')
    plt.ylim(ymax= n.max()*3.5/3)
    plt.show()
