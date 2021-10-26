"""
    Assignment advaced2 - Using decorator wrappings to handle data class
"""

import os
import logging
import math

import numpy as np
import matplotlib as plt
from scipy.interpolate import InterpolatedUnivariateSpline

class VoltageData:
    """ Class to handle time/voltage measuraments """

    def __init__(self, time, voltage):
        """ Class Constructor """
        assert len(time)==len(voltage)
        timestamps = np.array(time, dtype = np.float64)
        voltages = np.array(voltage, dtype = np.float64)
        self._data = np.column_stack((timestamps,voltages))
        self._spline = InterpolatedUnivariateSpline(timestamps, voltages, k=3)

    @classmethod
    def from_file(cls, file_path):
        """ Metodo per creare oggetto 'cls' che contiene le risorse
            da un file di testo. Necessario usare '@classmethod' che
            emula il costruttore
        """
        t, v = numpy.loadtxt(file_path, unpack = True)
        return cls()

    @property
    def timestamps(self):
        """ Accede ai dati di tempo """
        return self._data(:,0)

    @property
    def voltages(self):
        """ Accede ai dati di tensione """
        return self._data(:,1)

    def __len__(self):
        """ lenght method """
        return len(self._data)

    def __getitem__(self, index):
        """ Metodo speciale per accedere ad un elemento con [] """
        return self._data(index)

    def __iter__(self):
        """ Definisco esplicitamente l'iteratore, anche se python
            lo implementa di default se ho inizializzato len e getitem
        """
        #for row in data:
        #    yield row
        return iter(self._data)

    def __repr__(self):
        """ Implementato così per l'assignment: list comprhension
            su un generatore join()
        """
        return '\n'.join((f'{row[0]} {row[1]}' for row in self))

    def __str__(self):
        """ Print carino """
        rows = ['f{i}->{row[0]}{row[1]}' for i, row in enumerate(self)]
        return '\n'.join(rows)

    def __call__(self, time):
        """ Call method sulla spline """
        return self._spline(time)

    def plot(self):
        """ Implementare da solo
        """






    pass
