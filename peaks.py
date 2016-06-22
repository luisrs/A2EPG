from pylab import *
from numpy import NaN, Inf, arange, isscalar, array, asarray
import sys


def extract_y_coor(coordinates):
    values = [float(v_axis_y[1]) for v_axis_y in coordinates]
    return(array(values))


def find_peaks(v, delta, x=None):

    maxtab = []
    mintab = []
    if x is None:
        x = arange(len(v))
    v = asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    lookformax = True

    for i in arange(len(v)):
        axis_y = v[i]

        if axis_y > mx:
            mx = axis_y
            mxpos = x[i]
        if axis_y < mn:
            mn = axis_y
            mnpos = x[i]
        if lookformax:
            if axis_y < mx - delta:
                maxtab.append((mxpos, mx))
                mn = axis_y
                mnpos = x[i]
                lookformax = False
        else:
            if axis_y > mn + delta:
                mintab.append((mnpos, mn))
                mx = axis_y
                mxpos = x[i]
                lookformax = True
    return (maxtab), (mintab)


def plot(series):
    """ Function for plot a list of y_axis values (series), marking with
    red and green the maximum (maxtab) and minimum (mintab) values."""
    plot(series)
    scatter(array(maxtab)[:, 0], array(maxtab)[:, 1], color='green')
    scatter(array(mintab)[:, 0], array(mintab)[:, 1], color='red')
    show()
