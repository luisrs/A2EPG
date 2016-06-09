# def find_peaks(raw_data: List[float], ...) -> List[int]:
#     pass
# mark = EPGMark.from_file(datfile)
# peak_idxs = find_peaks(mark.raw_data)
# for i in peak_idxs:
# 	print(i, '=>', mark.raw_data[i], 'V')

from pylab import *
from numpy import NaN, Inf, arange, isscalar, array, asarray
import sys


def peakdet(v, delta, x=None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html

    Returns two arrays

    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.

    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.

    """
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
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        if lookformax:
            if this < mx - delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn + delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True
    return array(maxtab), array(mintab)

if __name__ == "__main__":
    from matplotlib.pyplot import plot, scatter, show

    # with open('APP&APA9-ch4.D0.dat', 'r') as f:
    with open('G+E1.dat', 'r') as f:
        lines = f.readlines()
    series = [float(x.strip()) for x in lines]

    # series = [5, 7, 8, 2, 10, 0, 15, -2, 0, 0, 0, 2, 0, 0, 0, -2, 0]
    # maxtab, mintab = peakdet(series, 0.3)
    # maxtab, mintab = peakdet(series, 0.2)
    maxtab, mintab = peakdet(series, 0.1)
    plot(series)
    scatter(array(maxtab)[:, 0], array(maxtab)[:, 1], color='green')
    scatter(array(mintab)[:, 0], array(mintab)[:, 1], color='red')
    show()
