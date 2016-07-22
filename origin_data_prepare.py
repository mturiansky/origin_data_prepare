#!/usr/bin/env python

'''
origin_data_prepare.py

A simple script to prepare Gamry DTA
files for import into OriginLab
'''

from argparse import ArgumentParser
from os.path import abspath, isdir, isfile, join
from os import listdir, mkdir
from shutil import rmtree
from sys import exc_info, stdout

import re

def file_handler(line, filename, output_file):
    '''
    analyzes the input line and filename
    and determines what to write to the output file
    '''
    regex = re.compile(r'(\t[^\t\n\r\f\v]+){8,}\n')
    if regex.match(line) is None:
        return

    regex = re.compile(r'\t')
    if 'CV' in filename or 'CA' in filename:
        split_line = regex.split(line)[3:5]
        try:
            split_line[1] = '%.5e' % (float(split_line[1])*1000000)
            a = split_line[1].split('e')
            a[1] = a[1][:1] + '0' + a[1][1:]
            split_line[1] = 'E'.join(a)
        except ValueError:
            if split_line[0] == 'Vf':
                split_line = ['Voltage', 'Current']
            else:
                split_line = ['V', 'uA']
    new_line = '\t' + '\t'.join(split_line) + '\n'
    output_file.write(new_line)

def dispatcher(dirty_path):
    '''
    looks through the path for DTA files
    and then selects the appropriate function for
    modifying the data
    '''
    print('[*] Opening path')
    path = abspath(dirty_path)
    if not isdir(path):
        raise ValueError('Not a directory')

    print('[*] Searching directory')
    filenames = [f for f in listdir(path) if isfile(join(path, f))]
    print('[+] Found %d files' % len(filenames))

    print('[*] Setting up output directory')
    output_path = join(path, 'output_data')
    try:
        mkdir(output_path)
    except FileExistsError:
        can_delete = input('[-] Directory exists, should we delete and continue? [Y/n]: ')
        if can_delete == 'Y' or can_delete == 'y':
            print('[*] Deleting old directory')
            rmtree(output_path)
            mkdir(output_path)
        else:
            raise
    print('[+] Directory created:', output_path)

    print('[*] Processing files')
    for f in filenames:
        print('[*] Current file:', f, end='\r')
        if 'DTA' not in f:
            continue
            
        with open(join(path, f), 'r') as opened_file:
            if 'CV' in f:
                output_path_filename = join(output_path, f) + 'CV'
            elif 'CA' in f:
                output_path_filename = join(output_path, f) + 'CA'
            else:
                output_path_filename = join(output_path, f)

            with open(output_path_filename, 'w') as output_file:
                for line in opened_file:
                    file_handler(line, f, output_file)
        stdout.write('\033[K')
    print('[+] Processing complete')

def setup_parser(parser):
    ''' adds arguments to the parser '''
    parser.add_argument('directory_path', help='path to the directory of DTA files')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

def main():
    ''' Main Function '''
    parser = ArgumentParser(description='A simple script to prepare Gamry'
                                        ' DTA files for import into OriginLab.')
    setup_parser(parser)
    args = parser.parse_args()
    try:
        dispatcher(args.directory_path)
    except Exception as err:
        exc_type = exc_info()[0]
        print('[-]', exc_type.__name__ + ':', err)

if __name__ == '__main__':
    main()
