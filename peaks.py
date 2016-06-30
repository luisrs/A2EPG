from pylab import *
from numpy import NaN, Inf, arange, isscalar, array, asarray
import sys
import argparse
import os
import numpy


class Peaks(object):
    """
    Peaks recieve the name of a EPGMark file, for generate the vector,
    which contains the y-axis values.
    """
    def __init__(self, mark=None):
        with open(mark, 'r') as markfile:
            lines = markfile.readlines()
        self.vector = [float(x.strip()) for x in lines]
        self.seconds = len(self.vector) / 100.0

    def find(self, x=None):

        delta = 0.005
        # self.maxs_peaks, self.mins_peaks = self.find(self.vector, 0.2)
        # self.measurements = (self.calculate_measurements())
        maxs = []
        mins = []
        if x is None:
            x = arange(len(self.vector))
        self.vector = asarray(self.vector)

        if len(self.vector) != len(x):
            sys.exit('Input vectors v and x must have same length')
        if not isscalar(delta):
            sys.exit('Input argument delta must be a scalar')
        if delta <= 0:
            sys.exit('Input argument delta must be positive')

        mn, mx = Inf, -Inf
        mnpos, mxpos = NaN, NaN
        lookformax = True

        for i in arange(len(self.vector)):
            axis_y = self.vector[i]

            if axis_y > mx:
                mx = axis_y
                mxpos = x[i]
            if axis_y < mn:
                mn = axis_y
                mnpos = x[i]
            if lookformax:
                if axis_y < mx - delta:
                    maxs.append((mxpos, mx))
                    mn = axis_y
                    mnpos = x[i]
                    lookformax = False
            else:
                if axis_y > mn + delta:
                    mins.append((mnpos, mn))
                    mx = axis_y
                    mxpos = x[i]
                    lookformax = True
        self.maxs = maxs
        self.mins = mins
        return (maxs), (mins)

    def plot(self):
        """ Function for plot a list of y_axis values (vector), marking with
        red and green the maximum (maxtab) and minimum (mintab) values."""
        plot(self.vector)
        scatter(
            array(self.maxs)[:, 0],
            array(self.maxs)[:, 1], color='green')
        scatter(
            array(self.mins)[:, 0],
            array(self.mins)[:, 1], color='red')
        show()


# parser = argparse.ArgumentParser()
# parser.add_argument('-dir', help='directory to read CSV and DAT files',
#                     action='store', dest='directory')
# args = parser.parse_args()
# peaks = Peaks(mark=args.directory)
# peaks.find()

# print("NMAXS")
# for nmax in peaks.maxs:
#     print(nmax[1])

# print("NMINS")
# for nmin in peaks.mins:
#     print(nmin[1])
# print(peaks.mins)
# frecuency, amplitude, var_max, var_min = peaks.return_measurements()
# print(
#     'Frecueny: {}\n Amplitude: {}\n Var_max:\n {}\n Var_min: {}'.format(
#         frecuency, amplitude, var_max, var_min))
# print('NMAXS')
# for nmax in peaks.maxs:
#     print(nmax[1])

# print('NMINS')
# for nmin in peaks.mins:
#     print(nmin[1])
# peaks.plot()
