#!/usr/bin/python

import argparse
import os
import glob
import itertools
# from enum import Enum
import csv
from peaks import find_peaks, extract_y_coor
import numpy


class EPGMark:

    def __init__(self, row, suffix, dat_infile):
        """TODO add docstring."""
        self.waveform = row[0]
        self.time_span = [(int(float(value) * 100)) for (value) in row[1:3]]
        print('self.time_span', self.time_span)
        self.seconds = (float(self.time_span[1]) - float(self.time_span[0])) / 100
        print('self.seconds', self.seconds)
        self.suffix = suffix
        self.dat_infile = dat_infile
        self.path = self.set_path()

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

    def calculate_measurements(self, maxs, mins):
        self.maxs_peaks = maxs
        self.mins_peaks = mins
        self.calculate_frecuency()
        self.calculate_amplitude()
        self.calculate_variation()

    def calculate_frecuency(self):
        cycles = 0
        for n_max, n_min in zip(self.maxs_peaks, self.mins_peaks):
            cycles += 1
        frecuency = (cycles / self.seconds)
        self.frecuency = frecuency

    def calculate_amplitude(self):

        # Amplitud v.1
        values_amplitude = list()
        for n_max, n_min in zip(self.maxs_peaks, self.mins_peaks):
            values_amplitude.append(float(n_max[1]) - float(n_min[1]))
        self.amplitude = (sum(values_amplitude) / len(values_amplitude))

        # Amplitud v.2
        max_values = extract_y_coor(self.maxs_peaks)
        min_values = extract_y_coor(self.mins_peaks)
        avg_max = numpy.mean(max_values)
        avg_min = numpy.mean(min_values)
        self.amplitude_v2 = (avg_max - avg_min)

    def calculate_variation(self):
        arr_max = numpy.array(self.maxs_peaks)
        self.desv_max = numpy.std(arr_max)
        arr_min = numpy.array(self.mins_peaks)
        self.desv_min = numpy.std(arr_min)


class Data(object):
    def __init__(self, dir=None, csv_infile=None):
        """TODO add docstring."""
        if(csv_infile is None):
            raise ValueError('Input file is required')
        self.dir = dir
        self.csv_infile = csv_infile

    def set_records(self):
        """TODO add docstring."""
        self.epg_marks = list()
        waveforms = list()
        dat_infile = os.path.splitext(self.csv_infile)[0] + '.dat'
        with open(self.csv_infile, 'r') as csv_file:
            spamreader = csv.reader(csv_file, delimiter=',', quotechar='|')
            suffix = 0
            for row in spamreader:
                self.epg_marks.append(
                    EPGMark(row, suffix, dat_infile))
                waveforms.append(row[0])
                suffix += 1
            self.type_waveforms = list(set(waveforms))
        self.create_folders()
        return(self.epg_marks)

    def create_folders(self):
        """Create the output and waveforms folders."""
        if not os.path.exists(self.dir.output):
                os.makedirs(self.dir.output)
        for n_folder in self.type_waveforms:
            if not os.path.exists(os.path.join(self.dir.output, n_folder)):
                os.makedirs(os.path.join(self.dir.output, n_folder))

parser = argparse.ArgumentParser()
parser.add_argument('-dir', help='directory to read CSV and DAT files',
                    action='store', dest='directory')
parser.add_argument('-o', help='directory to save the results',
                    action='store', dest='output')
args = parser.parse_args()
ROOT_DIR = args.output

os.chdir(args.directory)
for file in glob.glob("*.csv"):
    print("Splitting {}...".format(file))
    data = Data(dir=args, csv_infile=file)
    marks = data.set_records()
    print("done")

for mark in marks:
    print(mark.path)
    mark.write()
    with open(mark.path, 'r') as f:
        lines = f.readlines()
    series = [float(x.strip()) for x in lines]
    max_peaks, min_peaks = find_peaks(series, 0.005)
    mark.calculate_measurements(max_peaks, min_peaks)
    data_file = os.path.join(ROOT_DIR, 'EPGMarks_Data.csv')
    with open(data_file, 'a+') as csvfile:
        spamwriter = csv.writer(
            csvfile,
            quotechar=',',
            quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([
            mark.waveform,
            mark.frecuency,
            mark.amplitude,
            # mark.amplitude_v2,
            mark.desv_max,
            mark.desv_min])
