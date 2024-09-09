# -*- coding: utf-8 -*-
# Author  : Marcio Katsumi Yamashita
#           marcio.yamashita@fugro.com
# Date    : 2024-07-06 9:23
# Goal    : Concat binary file for NTL by year
import os
import shutil
from fnmatch import fnmatch


years = ["2022", "2023", "2024"]

for year in years:
    output_base_dir = os.path.join(os.path.curdir, f'data/{year}' )
    pattern = '42373*bin'
    fext = open(f'ADCP_42373_{year}.bin', 'wb')

    for path, subdirs, files in os.walk(output_base_dir):
        for name in files:
            if fnmatch(name, pattern):
                print(os.path.join(path, name))
                fo = open(os.path.join(path, name), "rb")
                shutil.copyfileobj(fo, fext, 65536)
                fo.close()  
    fext.close()
