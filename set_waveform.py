#!/usr/bin/python

import argparse
import os
import glob
import itertools
import csv
from numpy import array
import numpy
from peaks import Peaks


WaveForm_alias = {'C': '0', 'Pd': '1', 'G': '2', 'F': '3', 'E1': '4', 'Np':'5'}


class EPGMark(object):

    def __init__(self, row, suffix, dat_infile):
        """TODO add docstring."""
        self.waveform = row[0]
        self.time_span = [(int(float(value) * 100)) for (value) in row[1:3]]
        # print('self.time_span', self.time_span)
        self.seconds = (float(self.time_span[1]) - float(self.time_span[0])) / 100
        # if(self.seconds is 0):
        #     print("ESto es cero", self.waveform)
        # print('self.seconds', self.seconds)
        self.suffix = suffix
        self.dat_infile = dat_infile
        self.path = self.set_path()

    # @property
    # def path(self):
    #     return(self.path)

    def set_path(self):
        path = ('{}/{}{}.dat'.format(
            os.path.join(ROOT_DIR, self.waveform), self.waveform, self.suffix))
        return(path)

    def write(self):
        """TODO add docstring."""
        mark_file = open(self.path, "w+")
        with open(self.dat_infile) as dat_file:
            if(self.time_span[0] != 0):
                self.time_span[0] = self.time_span[0] - 1
            for line in itertools.islice(
                    dat_file, self.time_span[0], self.time_span[1]):
                mark_file.write(line)

    def find_peaks(self):
        peaks = Peaks(mark=self.path)
        self.maxs, self.mins = peaks.find()
        # peaks.plot()
        # print("find_peaks")
        # print('self.maxs', self.maxs)
        # print('self.mins', self.mins)

    def calculate_measurements(self):
        measurements = Measurements(
            maxs=self.maxs,
            mins=self.mins,
            seconds=self.seconds)
        self.frecuency, self.amplitude, variation = measurements.calculate()
        self.var_max = variation[0]
        self.var_min = variation[1]
        self.avg_max = variation[2]
        self.avg_min = variation[3]


class Data(object):
    def __init__(self, dir=None, csv_infile=None):
        """TODO add docstring."""
        if(csv_infile is None):
            raise ValueError('Input file is required')
        self.dir = dir
        self.csv_infile = csv_infile

    def set_records(self, suffix):
        """TODO add docstring."""
        self.epg_marks = list()
        waveforms = list()
        dat_infile = os.path.splitext(self.csv_infile)[0] + '.dat'
        with open(self.csv_infile, 'r') as csv_file:
            spamreader = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in spamreader:
                if('Type' not in row):
                    self.epg_marks.append(
                        EPGMark(row, suffix, dat_infile))
                    waveforms.append(row[0])
                suffix += 1
            self.type_waveforms = list(set(waveforms))
        self.create_folders()
        return(self.epg_marks, suffix)

    def create_folders(self):
        """Create the output and waveforms folders."""
        if not os.path.exists(self.dir.output):
                os.makedirs(self.dir.output)
        for n_folder in self.type_waveforms:
            if not os.path.exists(os.path.join(self.dir.output, n_folder)):
                os.makedirs(os.path.join(self.dir.output, n_folder))


class Measurements(object):
    """docstring for Measurements"""
    def __init__(self, maxs=None, mins=None, seconds=None):
        self.maxs = maxs
        self.mins = mins
        self.seconds = seconds

    def calculate(self):
        self.calculate_frecuency()
        self.calculate_amplitude()
        self.calculate_variation()
        return(self.frecuency, self.amplitude, self.variation)

    def calculate_frecuency(self):
        cycles = 0
        for n_max, n_min in zip(self.maxs, self.mins):
            cycles += 1
        self.frecuency = (cycles / self.seconds)

    def calculate_amplitude(self):

        # Amplitud v.1
        values_amplitude = list()
        for n_max, n_min in zip(self.maxs, self.mins):
            values_amplitude.append(float(n_max[1]) - float(n_min[1]))
        if(len(values_amplitude) != 0):
            self.amplitude = (sum(values_amplitude) / len(values_amplitude))
            # print('amplitude', amplitude)
        else:
            self.amplitude = None

        # Amplitud v.2
        # max_values = extract_y_coor(maxs)
        # min_values = extract_y_coor(mins)
        # avg_max = numpy.mean(max_values)
        # avg_min = numpy.mean(min_values)
        # amplitude_v2 = (avg_max - avg_min)
        # print('amplitude_v2', amplitude_v2)

    def extract_y_coor(self, coordinates):
        values = [float(v_axis_y[1]) for v_axis_y in coordinates]
        return(array(values))

    def calculate_variation(self):
        arr_max = numpy.array(self.extract_y_coor(self.maxs))
        self.variation_maxs = round(numpy.std(arr_max), 3)
        arr_min = numpy.array(self.extract_y_coor(self.mins))
        self.variation_mins = round(numpy.std(arr_min), 3)
        avg_max = round(numpy.mean(self.extract_y_coor(self.maxs)), 3)
        avg_min = round(numpy.mean(self.extract_y_coor(self.mins)), 3)
        self.variation = [self.variation_maxs, self.variation_mins, avg_max, avg_min]

parser = argparse.ArgumentParser()
parser.add_argument('-dir', help='directory to read CSV and DAT files',
                    action='store', dest='directory')
parser.add_argument('-o', help='directory to save the results',
                    action='store', dest='output')
args = parser.parse_args()
ROOT_DIR = args.output
os.chdir(args.directory)
count_marks = 1

for file in glob.glob("*.csv"):
    print("Splitting {}...".format(file))
    data = Data(dir=args, csv_infile=file)
    marks, count_marks = data.set_records(count_marks)
    for mark in marks:
        mark.write()
        mark.find_peaks()
        mark.calculate_measurements()
        data_file = os.path.join(ROOT_DIR, 'EPGMarks_Data.csv')
        with open(data_file, 'a+') as csvfile:
            spamwriter = csv.writer(
                csvfile,
                quotechar=',',
                quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([
                mark.frecuency,
                mark.amplitude,
                mark.var_max,
                mark.var_min,
                mark.avg_max,
                mark.avg_min,
                mark.seconds,
                mark.waveform,
                WaveForm_alias[mark.waveform]])
    print("Done.")

# CONFIRM PEAKS VALUES
# peaks = Peaks(mark=args.directory)
# peaks.find()
# measurements = Measurements(maxs=peaks.maxs, mins=peaks.mins, seconds=peaks.seconds)
# frecuency, amplitude, variation = measurements.calculate()
# print(frecuency, amplitude, variation)
# peaks.plot()


