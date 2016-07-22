'''
origin_data_prepare.py

A simple script to prepare Gamry DTA
files for import into OriginLab
'''

from argparse import ArgumentParser
from os.path import abspath, isdir, isfile, join
from os import listdir, mkdir, rmdir
from sys import exc_info

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
            rmdir(output_path)
            mkdir(output_path)
        else:
            raise
    print('[+] Directory created:', output_path)

    print('[*] Processing files')
    for f in filenames:
        with open(join(path, f), 'r') as opened_file:
            with open(join(output_path, f), 'w') as output_file:
                for line in opened_file:
                    if 'CV' in f:
                        pass
                    elif 'LSV' in f:
                        pass
                    elif 'CA' in f:
                        pass

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
