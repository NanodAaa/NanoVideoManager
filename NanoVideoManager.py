import os
import sys
import shutil
import subprocess

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
    filelist_txt = open(os.path.join(install_path, "filelist.txt"), "w")
    for file in fileslist:
        if (file.endswith(".mp4") or file.endswith(".mkv") or file.endswith(".avi") or file.endswith(".flv") or file.endswith(".wmv")) and (not file.startswith("output.mp4")):
            filelist_txt.write("file '" + input_path + '\\' + file + "'\n")

    filelist_txt.close()

    filelist_txt = open(os.path.join(install_path, "filelist.txt"), "r")
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
    # print("# excute_cmd: " + excute_cmd + '\n')
    # os.system(excute_cmd)
    
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
    
    
def generate_folder(path):
    """ print('正在处理文件夹: ' + path) """
    dirs = os.listdir(path)
    for object in dirs:
        if os.path.isdir(os.path.join(path, object)):
            generate_folder(os.path.join(path, object))
        elif os.path.isfile(os.path.join(path, object)):
            if object.endswith('.jpg') or object.endswith('.png'):
                if os.path.exists(os.path.join(path, 'cover.jpg')):
                    """ print(os.path.join(path, 'cover.jpg'), '已存在') """
                else:
                    try:
                        """ print(os.path.join(path, object)) """
                        # 复制文件并重命名
                        """ print(os.path.join(path, 'cover.jpg')) # DEBUG """
                        shutil.copyfile(os.path.join(path, object), os.path.join(path, 'cover.jpg'))
                        print(os.path.join(path, object, 'cover.jpg'), '已生成')
                        # os.rename(os.path.join(path, object, file), os.path.join(path, object, 'cover.jpg'))
                    except OSError as e:
                        print(f'重命名失败: {e}')
                break  
                        
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
                # excute_cmd = 'ffmpeg -ss 3 -i input.mp4 -vf "select=gt(scene\,0.5)" -frames:v 5 -vsync vfr out%02d.jpg'
                #print("# excute_cmd: " + excute_cmd + '\n')
                #os.system(excute_cmd)
                
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

# 删除所有 nfo 文件
def delete_nfo_files(path):
    print('开始删除 nfo 文件')
    dirs = os.listdir(path)
    for object in dirs:
        if os.path.isdir(os.path.join(path, object)):
            print('正在处理文件夹: ', os.path.join(path, object))
            for file in os.listdir(os.path.join(path, object)):
                if file.endswith('.nfo'):
                    os.remove(os.path.join(path, object, file))
                    print(os.path.join(path, object, file), '已删除')
                else: 
                    continue

# -------------------------- Main -------------------------- #
print('\n'*2)
print('#'*100)
print('# NanoVideoMergerV0.1 - Merge Video Files')
print("# Author: NanodAaa (https://github.com/NanodAaa)\n")
print("# Please enter the input and output paths in the config.txt file.")
print('\n')

while 1:
    print("\n# Please select the functions you want to use:")
    function = input("# 0. Exit\n# 1. Merge files\n# 2. Jellyfin manager\n# 3. Generate thumbnails\n# Function: ")

    # Merge files
    if function == "1":
        print("# Merge files\n")
        
        install_path = os.path.abspath(__file__)
        install_path = os.path.dirname(install_path)
        print("# install_path: " + install_path + '#')
                
        input_path = input("# Please enter the path of the input folder: ")
        if not os.path.exists(input_path):
            print("# Path not exist! Exiting...")
            continue
        
        else:
            print ("# input_path: " + input_path)
            print ("# output_path: " + input_path)
            print('\n')
            get_file_list(input_path)

            if(input("# Continue to merge files? (y/n): ").lower() == 'y'):
                print("# Merging files\n")
                merge_files(os.path.join(install_path, "filelist.txt"), os.path.join(input_path, "output.mp4"))
            else:
                print("# Exiting...")
                continue
            
    # Jellyfin manager
    elif function == "2":
        while 1:
            print("# Jellyfin manager\n")
            print("\n# Please select the sub functions you want to use:")
            subFunction = input("# 0. Exit\n# 1. Generate thumbnails\n# 2. Delete nfo files\n# Sub function: ")
            if subFunction == "1":
                print("# Generating thumbnails\n")
                input_path = input("# Please enter the path of the folder: ")
                if not os.path.exists(input_path):
                    print("# Path not exist! Exiting...")
                    exit()
                generate_folder(input_path)
                
            elif subFunction == "2":
                while 1:
                    print("# Deleting nfo files")
                    input_path = input("# Please enter the path of the folder: ")
                    if not os.path.exists(input_path):
                        print("# Path not exist! Exiting...\n")
                        continue
                    
                    else:
                        delete_nfo_files(input_path)
                
            elif subFunction == "0":
                print("# Exiting...")
                break
                
            else:
                print("# Invalid input! Please try again.")
                
    # Generate thumbnails
    elif function == "3":
        print("# Generating thumbnails\n")
        input_path = input("# Please enter the path of the folder: ")
        if not os.path.exists(input_path):
            print("# Path not exist! Exiting...")
            continue
            
        else:
            get_video_list(input_path)
            if(input("# Continue to generate thumbnails? (y/n): ").lower() == 'y'):
                print("# Generating thumbnails...\n")
                generate_thumbnails(input_path)
                
            else:
                print("# Exiting...")
                continue

    elif function == "0":
        print("# Exiting...")
        exit()
            
    else:
        print("# Invalid input! Please try again.")


    print("\n# Done!\n")
    print('#'*100)
