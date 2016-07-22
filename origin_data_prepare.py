'''
origin_data_prepare.py

A simple script to prepare Gamry DTA
files for import into OriginLab
'''

from argparse import ArgumentParser
from os.path import abspath, isdir

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
    except Exception as e:
        print('[-]', e)

if __name__ == '__main__':
    main()
