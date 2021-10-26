"""
Assingnment 2: ProbabilityDensityFunction class
Algorithmn order : ~ n*log(n)
"""

import logging
import time
import sys
import unittest

import numpy as np
import matplotlib.pylab as plt
from scipy.interpolate import InterpolatedUnivariateSpline

#--------------------------------------------------------------

def inv_cumulative_func(spline, x_min, x_max):
    """ Compute the cumulative function of a pdf
    """
    norm = spline.integral(x_min, x_max)
    x_axis = np.linspace(x_min, x_max, 100)
    y_axis = np.array( [ spline.integral(x_min, value)/norm \
                        for value in x_axis ] )

    inv_func = InterpolatedUnivariateSpline(y_axis, x_axis, k=3)
    return inv_func

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
            logging.error("ERROR in definition of the data: \
            x and y arrays must have same lenght")
            sys.exit()
        if np.any(y<0) :
            logging.error(" ERROR in definition of the distribution: \
            y must be non-negative")
            sys.exit()
        self._order = order
        self._spline = InterpolatedUnivariateSpline(x, y, k = order)
        self._inv = inv_cumulative_func(self._spline, self._min, self._max)

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
        pdf_random = np.array([ self._inv(el) for el in random_value])
        return pdf_random

#--------------------------------------------------------------

def compute_algorithm_order():
    """ Function to compute the order of random algorithmn
    """
    tempo = []
    n_array = []
    number = 10
    while number < 10000001 :
        t_0 = time.time()
        x_array = np.linspace(0,1, number)
        y_array = np.exp(-(x_array-0.5)**2 *4)
        pdf = ProbDensFunc(x_array, y_array, order=3)
        pdf.random(number)
        t_fin = time.time()
        tempo.append(t_fin-t_0)
        n_array.append(number)
        print(f"{number} : tempo {t_fin-t_0}")
        number = number*10

    plt.plot(n_array, tempo)
    plt.xlabel('n')
    plt.ylabel('elapsed time')
    plt.grid(alpha = 0.75)
    plt.show()

#--------------------------------------------------------------

def throw_random():
    """ Function to generate histogram filled with random variable, given a
        certain distribution
    """
    number = 10000
    x_array = np.linspace(0,5, number)
    y_array = np.exp(-(x_array-2.5)**2 *4)
    pdf = ProbDensFunc(x_array, y_array, order=3)
    random_array = pdf.random(number)

    entries, bins, patches = plt.hist(x=random_array, bins='auto',
                         color='#0504aa',alpha=0.7, rwidth=0.85, density=True)
    plt.grid(alpha = 0.75)
    plt.xlabel('x value')
    plt.ylabel('occurences')
    plt.ylim(ymax= entries.max()*3.5/3)
    plt.show()

#--------------------------------------------------------------

class TestPdf(unittest.TestCase):
    """ Class to test ProbDensFunc class
    """

    def test_call(self):
        """ Testing call method in ProbDensFunc class """
        x_array = np.linspace( 0., 5., 10 )
        y_array = np.array( x_array*2 )
        pdf = ProbDensFunc(x_array, y_array, order=3)
        x_test = 2.5
        self.assertAlmostEqual(pdf(x_test), x_test*2)

    def test_compute_probability(self):
        """ Testing compute_probability method in ProbDensFunc class """
        x_array = np.linspace( 0., 5., 10 )
        y_array = np.array( x_array*2 )
        pdf = ProbDensFunc(x_array, y_array, order=3)
        self.assertAlmostEqual(pdf.compute_probability(0., 5.), 1)

#--------------------------------------------------------------

if __name__ == "__main__":

    throw_random()
    #compute_algorithm_order()
