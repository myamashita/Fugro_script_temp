#Steps to decode aquadopp
from glob import glob
import os

list_dir = glob('*.bin')
for f in list_dir:
    os.system(f'DecodeAquadopp "{f}"') 

#Steps in cmd prompt
for %f in (*.bin) do DecodeAquadopp.exe %f
