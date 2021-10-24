from merge_tiff import *
from caiman_process import *
from data_proc import *
from gui import *
import os
import time


"""
input_folder(str): default folder to use for input
    * Will look for all .tif files in input folder
    * tif file names should be formatted as:
        - '[fixed_component]_[changing_component].tif'
      where the fixed component is the same for all
      file names, and the changing component is some
      integer corresponding the the tif file ordering
output_folder(str): default folder to use for output
    * Will create an output file in this folder
output_file(str): default name of output file
    * Should end in '.hdf5'
fr(int): default framerate
"""
input_folder = 'C:/Users/right/Desktop/lab/raw data/2021-08-28/8PRT-20xobjective-001/'
output_folder = input_folder
output_file = 'TEST_OUT.hdf5'
fr = 4

# get input from gui
gui_input = run_gui(input_folder, output_folder, output_file, fr)
if gui_input is None:
    raise RuntimeError('No input')
input_folder, output_folder, output_file, fr = gui_input
print('--successful gui input--')

# ensure folders exist
while not os.path.exists(input_folder):
    time.sleep(1)
print('--found input folder--')
while not os.path.exists(output_folder):
    time.sleep(1)
print('--found output folder--')

# merge tif files
outfile = merge_tiff_from_folder(input_folder, output_folder)
print('--tiff files merged--')

print('outfile:', outfile)

# clean mmap files
for f in os.listdir(input_folder):
    if f.endswith('.mmap'):
        os.remove(os.path.join(input_folder, f))

# ensure merged tif file exists
merged_tif = outfile[0]
while not os.path.exists(merged_tif):
    time.sleep(1)
print('--found merged tif file--')

# process raw tif and output hdf5
outpath = os.path.join(output_folder, output_file)
caiman_main(fr, fnames=[merged_tif], out=outpath)
print('--raw tif file processed--')

# ensure hdf5 file exists
while not os.path.exists(outpath):
    time.sleep(1)
print('--found hdf5 file--')

# analyse hfile
hf = h5py.File(outpath, 'r')

