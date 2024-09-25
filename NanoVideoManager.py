import os
import sys
import shutil
import subprocess
from enum import Enum

# -------------------------- Macros ------------------------ #


# -------------------------- Data Structure ------------------------ #

# Main menu index dict
MenuDict = {'merge': '1', 
            'generate-thumb' : '2'
            }


# -------------------------- Functions ------------------------ #
def get_ffmpeg_path():
    """
    Get the ffmpeg.exe path in the project.

    Return: Absolute path of ffmpeg.exe in the project.
    """
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    if (sys.platform == 'win32'):   # windows
        ffmpeg_path = os.path.join(base_path, 'ffmpeg', 'bin', 'ffmpeg.exe')
        if (os.path.exists(ffmpeg_path)):
            return ffmpeg_path
        else:
            print('Get ffmpeg path failed!')
    
    else: # linux
        return os.path.join(base_path, 'ffmpeg', 'bin' , 'ffmpeg')

def get_file_list(input_path):
    """
    Get the file list and save it to filelist.txt.
    
    Args:
        `input_path`: the path of the input folder. 
    """
    fileslist = os.listdir(input_path)
    filelist_txt = open(os.path.join(INSTALL_PATH, "filelist.txt"), "w")
    for file in fileslist:
        if (file.endswith(".mp4") or file.endswith(".mkv") or file.endswith(".avi") or file.endswith(".flv") or file.endswith(".wmv")) and (not file.startswith("output.mp4")):
            filelist_txt.write("file '" + input_path + '\\' + file + "'\n")

    filelist_txt.close()

    filelist_txt = open(os.path.join(INSTALL_PATH, "filelist.txt"), "r")
    print("# filelist.txt: ")
    print(filelist_txt.read())
    filelist_txt.close()
    
def get_video_list(input_path):
    """ 
    Find all the video files in the input folder and display them on console.
    
    Args:
        `input_path`: the path of the input folder. 
    """
    fileslist = os.listdir(input_path)
    video_list = []
    for file in fileslist:
        if (file.endswith(".mp4") or file.endswith(".mkv") or file.endswith(".avi") or file.endswith(".flv") or file.endswith(".wmv")) or (file.endswith(".mov")) and (not file.startswith("output.mp4")):
            video_list.append(file)
            
    print("# Video list: ")    
    for video in video_list:
        print(video)

def merge_files(filelist_txt_path, output_path):
    """ 
    Merge the files in the filelist.txt to the output.mp4.
    
    Args:
        `filelist_txt_path`: the path of the filelist.txt.
        `output_path`: the path of the output.mp4.
    """
    # excute_cmd = 'ffmpeg -f concat -safe 0 -i ' + '"' + filelist_txt_path + '"' + ' -c copy ' + '"' + output_path + '"'
    
    ffmpeg_path = get_ffmpeg_path()
    command = [
        ffmpeg_path,
        '-f', 'concat',
        '-safe', '0', 
        '-i', filelist_txt_path,
        '-c', 'copy',
        output_path
    ]
    try:
        subprocess.run(command, check=True)
    
    except subprocess.CalledProcessError as e:
        print(f'ffmpeg process error! output:{e.returncode}')
                        
def generate_thumbnails(dir_path):
    """
    Generate thumbnails for all the video files in the input folder.
    
    Args:
        `dir_path`: the path of the input folder.
    """

    dirs = os.listdir(dir_path)
    for object in dirs:
        if os.path.isdir(os.path.join(dir_path, object)):
            generate_thumbnails(os.path.join(dir_path, object))
        elif os.path.isfile(os.path.join(dir_path, object)):
            if object.endswith('.mp4') or object.endswith('.mkv') or object.endswith('.avi') or object.endswith('.flv') or object.endswith('.wmv') or object.endswith('.mov'):
                # print(os.path.join(dir_path, object))
                # 调用 ffmpeg 生成缩略图
                input_path = os.path.join(dir_path, object)
                print("input_path: " + input_path)
                if (os.path.exists(os.path.join(dir_path, os.path.splitext(object)[0])) == False):
                    os.mkdir(os.path.join(dir_path, os.path.splitext(object)[0]))
                output_path = os.path.join(dir_path, os.path.splitext(object)[0], 'out%02d.jpg')
                
                ffmpeg_path = get_ffmpeg_path()
                command = [ffmpeg_path, 
                           '-ss', '3',
                           '-i', input_path, 
                           '-vf', 'select=gt(scene\,0.4)',
                           '-frames:v', '20', 
                           '-fps_mode', 'vfr',
                           output_path]
                try:
                    # Call subprocess to run FFMPEG command.
                    subprocess.run(command, check=True)
                
                except subprocess.CalledProcessError as e:
                    print(f'ffmpeg process error: {e.returncode}')
                
                
            else:
                pass

def menu_merge_videos():
    """
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
        get_file_list(input_path)

        if(input("# Continue to merge files? (y/n): ").lower() == 'y'):
            print("# Merging files\n")
            merge_files(os.path.join(INSTALL_PATH, "filelist.txt"), os.path.join(input_path, "output.mp4"))
        else:
            print("# Exiting...")
            return -1
        
    return 0

def menu_generate_thumb():
    """
    return: `0` if merge successfully. `-1` if failed.
    """
    input_path = input("# Please enter the path of the folder: ")
    if not os.path.exists(input_path):
        print("# Path not exist! Exiting...")
        return -1
        
    else:
        get_video_list(input_path)
        if(input("# Continue to generate thumbnails? (y/n): ").lower() == 'y'):
            print("# Generating thumbnails...\n")
            generate_thumbnails(input_path)
            
        else:
            print("# Exiting...")
            return -1
        
    return 0

# -------------------------- Main -------------------------- #
print('\n'*2)
print('#' + '-'*100 + '#')
print('# NanoVideoMergerV0.1 - Merge Video Files')
print("# Author: NanodAaa (https://github.com/NanodAaa)\n")
print('#' + '-'*100 + '#')
print('\n')

INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))
#print("# INSTALL_PATH: " + INSTALL_PATH + '#')     DEBUG

while 1:
    print(MenuDict)
    function = input("# Please select the functions you want to use: ")

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

    elif function == "0":
        print("# Exiting...")
        exit()
            
    else:
        print("# Invalid input! Please try again.")


    print("\n# Done!\n")
    print('#' + '-'*100 + '#')
