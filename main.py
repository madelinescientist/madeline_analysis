from merge_tiff import *
from caiman_process import *
from data_proc import *
from gui import *
from folder_scan import *
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
root_input_folder = 'F:/madeline_data/'
input_folders = {
    'F:/madeline_data/2021-07-15/8F1-001',
    'F:/madeline_data/2021-07-15/8F1-002',
    'F:/madeline_data/2021-07-15/8F1-003',
    'F:/madeline_data/2021-07-15/8F1-004',
    'F:/madeline_data/2021-07-15/8F1-005',
    'F:/madeline_data/2021-07-15/8F1-006',
    'F:/madeline_data/2021-07-15/8F2-001',
    'F:/madeline_data/2021-07-15/8F2-002',
    'F:/madeline_data/2021-07-16/8F2-001-1',
    'F:/madeline_data/2021-07-23/8F2-15min-018',
    'F:/madeline_data/2021-08-06/20x_objective-001',
    'F:/madeline_data/2021-08-28/8PRT-20xobjective-001',
    'F:/madeline_data/2021-09-17',
    'F:/madeline_data/JUV008/2021-10-31/JUV008-211031-gonogo-001',
    'F:/madeline_data/JUV008/2021-11-01/JUV008-211101-gonogo-001',
    'F:/madeline_data/JUV008/2021-11-02/JUV008-211102-005',
    'F:/madeline_data/JUV008/2021-11-02/JUV008-211102-gonogo-001',
    'F:/madeline_data/JUV008/2021-11-02/JUV008-211102-gonogo-002',
    'F:/madeline_data/JUV008/2021-11-02/JUV008-211102-gonogo-003',
    'F:/madeline_data/JUV008/2021-11-02/TSeries-11022021-1414-004',
    'F:/madeline_data/JUV008/2021-11-03/JUV008-211103-gonogo-001',
    'F:/madeline_data/JUV008/2021-11-04/JUV008-211104-gonogo-001',
    'F:/madeline_data/JUV008/2021-11-04/JUV008-211104-gonogo-002',
    'F:/madeline_data/JUV008/2021-11-05/JUV008-211105-gonogo-001',
    'F:/madeline_data/JUV009/2021-10-31/JUV009-211031-gonogo-001',
    'F:/madeline_data/JUV009/2021-11-01/JUV009-211101=gonogo-001',
    'F:/madeline_data/JUV009/2021-11-02/JUV009-211102-gonogo-001',
    'F:/madeline_data/JUV009/2021-11-03/JUV009-211103-gonogo-001',
    'F:/madeline_data/JUV009/2021-11-04/JUV009-211104-gonogo-001',
    'F:/madeline_data/JUV009/2021-11-04/JUV009-211104-gonogo-002',
    'F:/madeline_data/JUV009/2021-11-06/JUV009-211106-gonogo-001',
    'F:/madeline_data/JUV009/2021-11-07/JUV009-211107-gonogo-001',
    'F:/madeline_data/JUV009/2021-11-07/JUV009-211107-gonogo-002',
    'F:/madeline_data/JUV009/2021-11-08/JUV009-211108-gonogo-001'
}
output_folder = 'F:/madeline_data_output'
fr = 4

gui_enable = False
folder_scan_enable = False


# get input from gui
if gui_enable:
    gui_input = run_gui(root_input_folder, output_folder, fr)
    if gui_input is None:
        raise RuntimeError('No input')
    root_input_folder, output_folder, fr = gui_input
    print('--successful gui input--')

# ensure root and output folders exist
while not os.path.exists(root_input_folder):
    time.sleep(1)
print('--found input folder--')
while not os.path.exists(output_folder):
    time.sleep(1)
print('--found output folder--')

# folder scan starting at root input folder
if folder_scan_enable:
    input_folders = scan_folder(root_input_folder)
    print('--successful folder scan--')

# ensure input folders exist
for input_folder in input_folders:
    while not os.path.exists(input_folder):
        time.sleep(1)
print('--found all input folders--')

# analyze all input folders
for input_folder in input_folders:
    try:
        print(f'--BEGINNING PROCESSING OF INPUT FOLDER: {input_folder}--')
        outpath = os.path.join(output_folder, os.path.basename(input_folder) + '.hdf5')
        if os.path.exists(outpath):
            print('--skipping since folder already processed--')
            continue

        # merge tif files
        outfile = merge_tiff_from_folder(input_folder, output_folder)
        print('--tiff files merged--')

        # clean mmap files
        for f in os.listdir(output_folder):
            if f.endswith('.mmap'):
                os.remove(os.path.join(output_folder, f))

        # ensure merged tif file exists
        merged_tif = outfile[0]
        while not os.path.exists(merged_tif):
            time.sleep(1)
        print('--found merged tif file--')

        # process raw tif and output hdf5
        caiman_main(fr, fnames=[merged_tif], out=outpath)
        print('--raw tif file processed--')

        # ensure hdf5 file exists
        while not os.path.exists(outpath):
            time.sleep(1)
        print('--found hdf5 file--')
    except Exception as E:
        print(f'ERROR: processing of input folder failed: {input_folder}')
        print(E)
        f = open(outpath, 'w')
        f.close()

# analyse hfile
# hf = h5py.File(outpath, 'r')

