# -------------------------- Nano Video Manager ------------------------ #
# Author: NanodAaa 

import sys
import os
import sys
import subprocess
import vm
from enum import Enum, auto

# -------------------------- Macros ------------------------ #

# -------------------------- Data Structure ------------------------ #

class MenuIndex(Enum):
    """
    Enum for main menu function index.
    """
    merge = auto()
    merge_recode = auto()
    generate_thumb = auto()
    format_transformer = auto()

# Main menu index dict
MenuDict = {'merge': f'{MenuIndex.merge.value}',
            'merge-recode' : f'{MenuIndex.merge_recode.value}',
            'generate-thumb' : f'{MenuIndex.generate_thumb.value}',
            'format-transformer' : f'{MenuIndex.format_transformer.value}'
            }

# -------------------------- Functions ------------------------ #
def menu_merge_videos():
    """
    Merge Videos in folder into output.mp4
    
    return: `0` if merge successfully. `-1` if failed.
    """
    
    input_path = input("# Please enter the path of the input folder: ")
    if not os.path.exists(input_path):
        print("# Path not exist! Exiting...")
        return -1
    
    else:
        #print ("# input_path: " + input_path)          DEBUG
        #print ("# output_path: " + input_path)         DEBUG
        #print('\n')        DEBUG
        tool = vm.VideoMerger(input_path)
        
        if(input("# Continue to merge files? (y/n): ").lower() == 'y'):
            print("# Merging files\n")
            tool.merge_files()
        else:
            print("# Exiting...")
            return -1
        
    return 0

def menu_merge_videos_recode():
    """
    Merge videos by recoding.
    """

def menu_generate_thumb():
    """
    return: `0` if merge successfully. `-1` if failed.
    """
    input_path = input("# Please enter the path of the folder: ")
    #input_path = r'D:\DOWNLOAD\CACHE_SPACE\thumb test'
    if not os.path.exists(input_path):
        print("# Path not exist! Exiting...")
        return -1
        
    else:
        tool = vm.ThumbGenerator(input_path)
        if(input("# Continue to generate thumbnails? (y/n): ").lower() == 'y'):
            print("# Generating thumbnails...\n")
            tool.generate_thumbnails()
            
        else:
            print("# Exiting...")
            return -1
        
    return 0

def menu_format_transformer():
    """
    """
    input_path = input('Please input the path of video or folder to transform: ')
    if not os.path.exists(input_path):
        print('Path does not exist!')
        return -1
    
    else:
        output_format = input('Please input the output format (mp4, mkv, avi, flv): ')
        
        tool = vm.FormatTransformer(input_path, output_format)
        tool.format_transform()

    return

# -------------------------- Main -------------------------- #
print('\n'*2)
print('#' + '-'*100 + '#')
print('# NanoVideoMergerV0.1 - Merge Video Files')
print("# Author: NanodAaa (https://github.com/NanodAaa)\n")
print('#' + '-'*100 + '#')
print('\n')

#print("# INSTALL_PATH: " + INSTALL_PATH + '#')     DEBUG

while 1:
    print(MenuDict)
    function = input("# Please select the functions you want to use: ")
    #function = '3'

    # Merge files
    if function == MenuDict.get('merge'):
        print("# Merge files\n")
        ret = menu_merge_videos()
        if (ret):
            continue

    # Generate thumbnails
    elif function == MenuDict.get('generate-thumb'):
        print("# Generating thumbnails\n")
        ret = menu_generate_thumb()
        if (ret):
            continue

    # Format transformer
    elif function == MenuDict.get('format-transformer'):
        print('# Format Transformer\n')
        ret = menu_format_transformer()
        if ret:
            continue

    elif function == "0":
        print("# Exiting...")
        exit()

    else:
        print("# Invalid input! Please try again.")

    print("\n# Done!\n")
    print('#' + '-'*100 + '#')
