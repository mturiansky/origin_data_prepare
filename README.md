# origin_data_prepare

This project is a work in progress. Currently, it takes the directory path, searches it for DTA files, and puts the converted files into a subdirectory.

### To Do List

- LSV and EIS support
- More robust file handling
- Simple data analysis (avg, min, max)
- Multiprocessing support

### Usage

```
usage: origin_data_prepare.py [-h] [-v] [-s SHIFT] [-o OUTDIR]
                              [-u {A,mA,uA,nA}] [-m] [-d]
                              directory_path

A simple script to prepare Gamry DTA files for import into OriginLab.

positional arguments:
  directory_path        path to the directory of DTA files

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -s SHIFT, --shift SHIFT
                        apply a voltage shift to CV data
  -o OUTDIR, --outdir OUTDIR
                        specify the output directory name
  -u {A,mA,uA,nA}, --units {A,mA,uA,nA}
                        specify the units of the current output
  -m, --multiprocess    enable use of multiprocessing to speed up program
  -d, --debug           provide extra debugging output
```
