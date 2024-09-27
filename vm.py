import sys
import os
import sys
import subprocess

class VideoManager:
    """
    """
    INSTALL_PATH = ''
    FFMPEG_PATH = ''
    INPUT_PATH = ''
    
    def __init__(self):
        self.FFMPEG_PATH = self.get_ffmpeg_path()
        self.INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))
    
    def get_ffmpeg_path(self):
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
        
    def get_video_list(self):
        """ 
        Find all the video files in the input folder and display them on console.
        """
        fileslist = os.listdir(self.INPUT_PATH)
        video_list = []
        for file in fileslist:
            if (file.endswith(".mp4") or file.endswith(".mkv") or file.endswith(".avi") or file.endswith(".flv") or file.endswith(".wmv")) or (file.endswith(".mov")) and (not file.startswith("output.mp4")):
                video_list.append(file)
                
        print("# Video list: ")    
        for video in video_list:
            print(video)
        
    def get_video_info(self):
        """
        Get video info: Frame rate, Resoulation, time...
        
        Args:
            `input_path`: 
        
        Return:

        """
        
        if not os.path.exists(self.INPUT_PATH):
            print('Input path does not exist.')
            return -1
        
        command = [
            self.FFMPEG_PATH,
            '-i', self.INPUT_PATH,
            '-f', 'json',
            '-hide_banner'
        ]
        
        result = subprocess.run(command, stderr=subprocess.PIPE, universal_newlines=True)
        
class VideoMerger(VideoManager):
    """
    
    """
    FILELIST_TXT_PATH = ''
    
    def __init__(self, input_path):
        super().__init__()
        self.FILELIST_TXT_PATH = os.path.join(self.INSTALL_PATH, "filelist.txt")
        self.INPUT_PATH = input_path
        
    def get_filelist_txt(self):
        """
        Get the video list and save it to filelist.txt.
        
        Args:
            `input_path`: the path of the input folder. 
        """
        fileslist = os.listdir(self.INPUT_PATH)
        filelist_txt = open(self.FILELIST_TXT_PATH, "w")
        for file in fileslist:
            if (file.endswith(".mp4") or file.endswith(".mkv") or file.endswith(".avi") or file.endswith(".flv") or file.endswith(".wmv")) and (not file.startswith("output.mp4")):
                filelist_txt.write("file '" + self.INPUT_PATH + '\\' + file + "'\n")
                
        print("# filelist.txt: ")
        # print(filelist_txt.read())
        filelist_txt.close()
        
    def merge_files(self, output_path=None):
        """ 
        Merge the files in the filelist.txt to the output.mp4.
        
        Args:
            `input_path`: the path of the folder which contain the videos to merge.
            `output_path`: the path of the output.mp4.
        """
        # excute_cmd = 'ffmpeg -f concat -safe 0 -i ' + '"' + filelist_txt_path + '"' + ' -c copy ' + '"' + output_path + '"'
        
        if (output_path == None):
            output_path = os.path.join(self.INPUT_PATH, "output.mp4")
        
        self.get_filelist_txt()
        command = [
            self.FFMPEG_PATH,
            '-f', 'concat',
            '-safe', '0', 
            '-i', self.FILELIST_TXT_PATH,
            '-fflags', '+genpts',  # 添加此行以强制生成时间戳
            '-c', 'copy',
            output_path
        ]
        try:
            subprocess.run(command, check=True)
        
        except subprocess.CalledProcessError as e:
            print(f'ffmpeg process error! output:{e.returncode}')
            
class ThumbGenerator(VideoManager):
    """
    """
    INPUT_PATH = ''
    CURRENT_PATH = ''
    
    def __init__(self, input_path):
        super().__init__()
        self.INPUT_PATH = input_path
        self.CURRENT_PATH = self.INPUT_PATH
    
    def generate_thumbnails(self):
        """
        Generate thumbnails for all the video files in the input folder.
        
        Args:
            `dir_path`: the path of the input folder.
        """

        dirs = os.listdir(self.CURRENT_PATH)
        for object in dirs:
            object_path = os.path.join(self.CURRENT_PATH, object)
            if os.path.isdir(object_path):
                self.CURRENT_PATH = object_path
                self.generate_thumbnails()
            else:
                if object.endswith('.mp4') or object.endswith('.mkv') or object.endswith('.avi') or object.endswith('.flv') or object.endswith('.wmv') or object.endswith('.mov'):
                    # print(os.path.join(dir_path, object))
                    # 调用 ffmpeg 生成缩略图
                    # print("input_path: " + input_path)    DEBUG
                    input_path = object_path
                    output_path = os.path.join(self.INPUT_PATH, os.path.splitext(object)[0])
                    if (os.path.exists(output_path) == False):
                        os.mkdir(output_path)
                        
                    else:
                        output_path = os.path.join(output_path, 'out%02d.jpg')
                    
                    command = [self.FFMPEG_PATH, 
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
        
            self.CURRENT_PATH = os.path.split(self.CURRENT_PATH)[0]
            