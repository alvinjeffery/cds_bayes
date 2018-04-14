

import numpy as np 
import sys, os 


INPUT_FILES_PATH = "/Users/abin-personal/Google Drive/1_MSTP/2_Research/1_CapraLab/courses/BMIF6315/assignments/clinical_decision_support/clin_decis_support_assignment/DX"
INPUT_FILE_NAMES = [ "DX1", "DX2", "DX3", "DX4", "DX5", "DX6", "DX7", "DX8", "DX9", "DX10"] 



# =============  functions =============


# =============  main =============


ppv_greater_than = 3
ppv_less_than = 1

high_ppv_list = []
low_ppv_list = [] 


for one_file in INPUT_FILE_NAMES: 

    this_file = os.path.join(INPUT_FILES_PATH, one_file)
    with open(this_file) as f:
        for num, line in enumerate(f):

            if num == 0: 
                dx_name = line.split()[2:]
                print(" ".join(dx_name))
                high_ppv_list.append(line)
                low_ppv_list.append(line)


            if num != 0 : 
                ppv = line.split()[1][0]
                sens = line.split()[1][1] 

                if int(ppv) >= ppv_greater_than: 
                    high_ppv_list.append(line)
                elif int(ppv) <= ppv_less_than: 
                    low_ppv_list.append(line) 


    high_file_out = os.path.join(INPUT_FILES_PATH, "test_set", one_file + "_high.txt")
    low_file_out = os.path.join(INPUT_FILES_PATH, "test_set", one_file + "_low.txt")

    with open(high_file_out, 'w') as fh:
        for item in high_ppv_list:
            fh.write(item)


    with open(low_file_out, 'w') as fh:
        for item in low_ppv_list:
            fh.write(item)
            