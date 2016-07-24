#!/usr/bin/env python

'''
origin_data_prepare.py

A simple script to prepare Gamry DTA
files for import into OriginLab
'''

from argparse import ArgumentParser
from multiprocessing import Pool
from os.path import abspath, isdir, isfile, join
from os import listdir, mkdir
from shutil import rmtree
from sys import exc_info, stdout

import re

UNIT_CONV = {'A':1, 'mA':1000, 'uA':1000000, 'nA':1000000000}

def sci_not_format(num):
    ''' formats number with 5 decimal places and 3 exponent places '''
    snum = '%.5e' % num
    a = snum.split('e')
    a[1] = a[1][:1] + '0' + a[1][1:]
    return 'E'.join(a)

def mod_filename(path, filename):
    ''' determines the file type and appends to the end '''
    joined_path = join(path, filename)
    if 'CV' in filename:
        return joined_path + 'CV'
    elif 'CA' in filename:
        return joined_path + 'CA'
    else:
        return joined_path

def file_handler(line, filename, output_file, shift, units):
    '''
    analyzes the input line and filename
    and determines what to write to the output file
    '''
    # skip lines that don't match pattern
    regex = re.compile(r'(\t[^\t\n\r\f\v]+){8,}\n')
    if regex.match(line) is None:
        return

    # split lines and determine what to keep
    regex = re.compile(r'\t')
    split_line = regex.split(line)
    if 'CV' in filename:
        selected = split_line[3:5]
    elif 'CA' in filename:
        selected = split_line[2:5:2]
    else:
        selected = split_line

    try:
        if 'CV' in filename:
            selected[1] = sci_not_format(float(selected[1])*UNIT_CONV[units])
            if shift is not None:
                selected[0] = sci_not_format(float(selected[0])+shift)
        elif 'CA' in filename:
            selected[0] = selected[0] # need to figure out time scaling
            selected[1] = sci_not_format(float(selected[1])*UNIT_CONV[units])
    except ValueError:
        if 'CV' in filename:
            if selected[0] == 'Vf':
                selected = ['Voltage', 'Current']
            else:
                selected = ['V', units]
        elif 'CA' in filename:
            if selected[0] == 'T':
                selected = ['Time', 'Current']
            else:
                selected = ['s', units]

    new_line = '\t' + '\t'.join(selected) + '\n'
    output_file.write(new_line)

def file_opener(path, filename, output_path, shift, units):
    '''
    opens two files, one for reading, one for writing
    passes each line to the file_handler
    having this separate function is necessary for
    multiprocessing
    '''
    with open(join(path, filename), 'r') as opened_file:
        output_path_filename = mod_filename(output_path, filename)
        with open(output_path_filename, 'w') as output_file:
            for line in opened_file:
                file_handler(line, filename, output_file, shift, units)

def dispatcher(args):
    '''
    looks through the path for DTA files
    and then selects the appropriate function for
    modifying the data
    '''
    path = abspath(args.directory_path)
    if not isdir(path):
        raise ValueError('Not a directory')

    print('[*] Searching directory')
    filenames = [f for f in listdir(path) if isfile(join(path, f)) and 'DTA' in f]
    print('[+] Found %d files' % len(filenames))

    print('[*] Setting up output directory')
    output_path = join(path, args.outdir)

    try:
        mkdir(output_path)
    except FileExistsError:
        can_delete = input('[-] Directory \'' + output_path + '\' exists, should we delete and continue? [Y/n]: ')
        if can_delete == 'Y' or can_delete == 'y':
            print('[*] Deleting old directory')
            rmtree(output_path)
            mkdir(output_path)
        else:
            print('[-] Please handle the old directory or use the \'--outdir\' flag to specify a new output path.')
            raise
    print('[+] Directory created:', output_path)

    print('[*] Processing files')
    if args.multiprocess:
        pool = Pool(processes=4)
        for f in filenames:
            pool.apply_async(func=file_opener, args=(path, f, output_path, args.shift, args.units))
        pool.close()
        pool.join()
    else:
        for i,f in enumerate(filenames):
            print('[*] Current file (' + str(i) + '/' + str(len(filenames)) + '):', f, end='\r')
            file_opener(path, f, output_path, args.shift, args.units)
            stdout.write('\033[K')
    print('[+] Processing complete')

def setup_parser(parser):
    ''' adds arguments to the parser '''
    parser.add_argument('directory_path', help='path to the directory of DTA files')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.2')
    parser.add_argument('-s', '--shift', action='store', type=float,
                        help='apply a voltage shift to CV data')
    parser.add_argument('-o', '--outdir', action='store', default='output_data',
                        help='specify the output directory name')
    parser.add_argument('-u', '--units', action='store', default='A',
                        choices=['A', 'mA', 'uA', 'nA'], help='specify the units of the current output')
    parser.add_argument('-m', '--multiprocess', action='store_true',
                        help='enable use of multiprocessing to speed up program')
    parser.add_argument('-d', '--debug', action='store_true', help='provide extra debugging output')

def main():
    ''' Main Function '''
    parser = ArgumentParser(description='A simple script to prepare Gamry'
                                        ' DTA files for import into OriginLab.')
    setup_parser(parser)
    args = parser.parse_args()

    if (args.debug):
        print('[D] directory_path:', args.directory_path)
        print('[D] output directory:', args.outdir)
        print('[D] units:', args.units)
        if args.shift is not None:
            print('[D] shift:', sci_not_format(args.shift))
        else:
            print('[D] shift: None')
        print('[D] multiprocess:', args.multiprocess)

    try:
        dispatcher(args)
    except Exception as err:
        exc_type = exc_info()[0]
        print('[-]', exc_type.__name__ + ':', err)
    finally:
        print('[+] Exitting')

if __name__ == '__main__':
    main()
