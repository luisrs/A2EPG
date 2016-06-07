#!/usr/bin/python

import argparse
import os
import glob
import itertools
from enum import Enum
import csv


class WaveForm(Enum):
    np = 'No penetration'
    c = 'Salivation Intracellular'
    pd = 'Cell punctures'               # Pinchazos celulares
    g = 'Xylem ingestion'
    f = 'Penetration difficulties'
    e1 = 'salivation'
    e2 = 'ingestion'


class EPGProfile:
    def __init__(self, marks=()):
        self.marks = tuple(marks)

    @staticmethod
    def from_file(csvfile):
        pass


class EPGMark:
    """"asdasd ."""

    def __init__(self, row, suffix, dat_infile):
        """TODO add docstring."""
        self.waveform = row[0]
        self.time_span = [(int(float(value) * 100)) for (value) in row[1:3]]
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
            for line in itertools.islice(dat_file, self.time_span[0], self.time_span[1]):
                mark_file.write(line)

    @staticmethod
    def from_file(dat_fragment):
        num_lines = sum(1 for line in open(dat_fragment))
        print('dat_fragment', num_lines)


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
    print('\n')

# for mark in marks:
#     filename = ...
#     mark.write(filename)

for mark in marks:
    print(mark.path)
    EPGMark.from_file(mark.path)

# for datfile in glob.glob('*.dat'):
#     mark = EPGMark.from_file(datfile)

# # ------------------------

# def find_peaks(raw_data: List[float], ...) -> List[int]:
#     pass

# mark = EPGMark.from_file(datfile)
# peak_idxs = find_peaks(mark.raw_data)
# for i in peak_idxs:
#     print(i, '=>', mark.raw_data[i], 'V')
