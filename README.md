# origin_data_prepare

This project is a work in progress. Currently, it takes the directory path, searches it for DTA files, and puts the converted files into a subdirectory.

### To Do List

- Select the units for the current output
- Specify a different output directory
- More robust file handling

### Usage

```
usage: origin_data_prepare.py [-h] [-v] directory_path

A simple script to prepare Gamry DTA files for import into OriginLab.

positional arguments:
  directory_path  path to the directory of DTA files

optional arguments:
  -h, --help      show this help message and exit
  -v, --version   show program's version number and exit
```
