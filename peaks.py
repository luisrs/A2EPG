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
    # return array(maxtab), array(mintab)

# parser = argparse.ArgumentParser()
# parser.add_argument('-infile', help='directory to read CSV and DAT files',
#                     action='store', dest='infile')
# args = parser.parse_args()


# if __name__ == "__main__":
#     from matplotlib.pyplot import plot, scatter, show
# # SERIES
#     # with open(args.infile, 'r') as f:
#     #     lines = f.readlines()
#     # series = [float(x.strip()) for x in lines]
#     series = [0, 1, 3, 1, 2, 3, 1, 0, 1, 3, 1, 2, 3, 1, 0, 1, 3, 1, 2, 3, 1]

# # PROCESS TIME
#     start_time = time.time()
#     maxtab, mintab = find_peaks(series, 0.005)
#     print("%s seconds" % (time.time() - start_time))

# # FRECUENCY
# # a)
#     cycles = 0
#     for n_max, n_min in zip(maxtab, mintab):
#         cycles += 1
#     frecuency = (cycles / seconds)
#     print('Frecuency ({}) = cyles ({}) / seconds ({})'.format(
#         frecuency, cycles, seconds))

# # AMPLITUD
# # b).1

#     values_amplitude = list()
#     for n_max, n_min in zip(maxtab, mintab):
#         print(n_max[1], n_min[1])
#         values_amplitude.append(float(n_max[1]) - float(n_min[1]))
#     amplitude = (sum(values_amplitude) / len(values_amplitude))
#     print(values_amplitude)
#     print('amplitude b.1', amplitude)

# # b).2

#     def extract_values(coordinates):
#         values = [float(v_axis_y[1]) for v_axis_y in coordinates]
#         return(array(values))

#     max_values = extract_values(maxtab)
#     min_values = extract_values(mintab)
#     avg_max = numpy.mean(max_values)
#     avg_min = numpy.mean(min_values)
#     amplitude = (avg_max - avg_min)
#     print('amplitude b.2', amplitude)

# # VARIACION ENTRE MAX Y MIN
# # c)
#     arr_max = numpy.array(max_values)
#     desv_max = numpy.std(arr_max)
#     arr_min = numpy.array(min_values)
#     desv_min = numpy.std(arr_min)
#     print('desv_max, desv_min', desv_max, desv_min)


# # PLOT
#     plot(series)
#     scatter(array(maxtab)[:, 0], array(maxtab)[:, 1], color='green')
#     scatter(array(mintab)[:, 0], array(mintab)[:, 1], color='red')
#     show()
