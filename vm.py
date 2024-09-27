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
    VIDEO_LIST = []
    
    def __init__(self, input_path):
        self.FFMPEG_PATH = self.get_ffmpeg_path()
        self.INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))
        self.INPUT_PATH = input_path
        self.VIDEO_LIST = self.get_video_list()
    
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
        
    def get_video_list(self, input_path=None):
        """ 
        Find all the video files in the input folder and display them on console.
        
        Args:
            `input_path`: The path of the video or folder which contain the videos. Default = None.
        
        Return:
            `video_list`: List include video name, video abspath and other video info.
        """
        
        video_list = []
        
        if input_path == None:
            input_path = self.INPUT_PATH
            
        if os.path.isfile(input_path):
            video_list = [
                {
                    'basename' : os.path.basename(input_path),
                    'dirname' : os.path.split(input_path)[0],
                    'format' : os.path.splitext(os.path.basename(input_path))[1],
                    'abspath' : input_path
                }
            ]
            return video_list
        
        fileslist = os.listdir(input_path)
        for file in fileslist:
            if (file.endswith(('mp4', 'mkv', 'avi', 'flv', 'mov'))) and (not file.startswith("output.mp4")):
                basename = file
                dirname = input_path
                format = os.path.splitext(basename)[1]
                abspath = os.path.join(input_path, file)
                
                video_list.append(
                    {
                        'basename' : basename,
                        'dirname' : dirname,
                        'format' : format,
                        'abspath' : abspath
                    }
                )
                
        print("# Video list: ")    
        for video in video_list:
            print(f"Filename: {video['basename']}, File abspath: {video['abspath']}")
            
        return video_list
        
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
        super().__init__(input_path)
        self.FILELIST_TXT_PATH = os.path.join(self.INSTALL_PATH, "filelist.txt")
        
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
    CURRENT_PATH = ''
    
    def __init__(self, input_path):
        super().__init__(input_path)
        self.CURRENT_PATH = self.INPUT_PATH
    
    def generate_thumbnails(self):
        """
        Generate thumbnails for all the video files in the input folder.
        
        Args:
            `dir_path`: the path of the input folder.
        """

        for video in self.VIDEO_LIST:
            output_path = os.path.join(video['dirname'], os.path.splitext(video['basename'])[0])
            if (os.path.exists(output_path) == False):
                os.mkdir(output_path)
                
            output_path = os.path.join(output_path, 'out%02d.jpg')
            
            command = [self.FFMPEG_PATH, 
                            '-ss', '3',
                            '-i', video['abspath'], 
                            '-vf', 'select=gt(scene\,0.4)',
                            '-frames:v', '20', 
                            '-fps_mode', 'vfr',
                            output_path]
            try:
                # Call subprocess to run FFMPEG command.
                subprocess.run(command, check=True)
            
            except subprocess.CalledProcessError as e:
                print(f'ffmpeg process error: {e.returncode}')
                
        return
            
class FormatTransformer(VideoManager):
    """
    """
    OUTPUT_FORMAT = ''
    VALID_OUTPUT_FORMAT_TUPLE = ('mp4', 'mkv', 'avi', 'mov', 'flv')
    
    def __init__(self, input_path, output_format):
        super().__init__(input_path)
        self.OUTPUT_FORMAT = output_format
        
    def format_transform(self, input_path=None, output_format=None):
        """
        Transform video format.
        """
        
        if not input_path == None:
            video_list = self.get_video_list()
            
        else:
            input_path = self.INPUT_PATH
            video_list = self.VIDEO_LIST
            
        if not os.path.exists(input_path):
            print('File does not exist!')
            return -1
            
        if output_format == None:
            output_format = self.OUTPUT_FORMAT
            
        if not output_format in self.VALID_OUTPUT_FORMAT_TUPLE:
            print('Output format is invalid!')
            return -1
        
        recode_flag = False
        if (input('Wether you want to recode the video? (y/n): ').lower == 'y'):
            recode_flag = True
            
        else:
            for video in video_list:
                
                command = [
                    self.FFMPEG_PATH,
                    '-i', video['abspath'],
                ]
                
                if recode_flag == False:
                    command.append('-c')
                    command.append('copy')
                    
                output_path = os.path.join(video['dirname'], 
                                                os.path.splitext(video['basename'])[0]) + f'.{output_format}'
                command.append(output_path)
                
                try:
                    subprocess.run(command, check=True)
                    
                except subprocess.CalledProcessError as e:
                    print(f'{e.returncode}')
                    return -1
            
class VideoSpilter(VideoManager):
    """
    """
    def __init__(self, input_path):
        super().__init__(input_path)
        
    def video_spilt(self, spilt_size):
        
        for video in self.VIDEO_LIST:
            
            output_path = os.path.join(video['dirname'], os.path.splitext(video['basename'])[0])
            if not os.path.exists(output_path):
                os.mkdir(output_path)
                
            output_path = os.path.join(output_path, 'output%02d.mp4')
            
            command = [
                self.FFMPEG_PATH,
                '-i', video['abspath'],
                '-fs', spilt_size,
                '-c', 'copy',
                output_path
            ]
            
            try:
                subprocess.run(command)
                
            except subprocess.CalledProcessError as e:
                print(f'Video spilt failed! Return code: {e.returncode}')
                return -1
            
        return