import os
import subprocess
from enum import Enum, auto

class VideoManager:
    """
    """
    INSTALL_PATH = ''
    FFMPEG_PATH = ''
    FFPROBE_PATH = ''
    INPUT_PATH = ''
    VIDEO_LIST = []
    
    def __init__(self, input_path, install_path):
        self.INSTALL_PATH = install_path
        self.FFMPEG_PATH = self.get_ffmpeg_path()
        self.FFPROBE_PATH = self.get_ffprobe_path()
        self.INPUT_PATH = input_path
        self.VIDEO_LIST = self.get_video_list()
    
    def get_ffmpeg_path(self):
        """
        Get the ffmpeg.exe path in the project.
        """           
        for root, dir, file in os.walk(self.INSTALL_PATH):
            if 'ffmpeg.exe' in file:
                return os.path.join(root, 'ffmpeg.exe')
        
    def get_ffprobe_path(self):
        """
        Get the ffprobe.exe path in the project.
        """
        for root, dir, file in os.walk(self.INSTALL_PATH):
            if 'ffprobe.exe' in file:
                return os.path.join(root, 'ffprobe.exe')
        
    def get_video_list(self, input_path=None):
        """ 
        Find all the video files in the input folder and display them on console.
        
        Args:
            `input_path`: The path of the video or folder which contain the videos. Default = None.
        
        Returns:
            `video_list`: List include video name, video abspath and other video info.
        """
        
        video_list = []
        
        if input_path == None:
            input_path = self.INPUT_PATH
            
        if os.path.isfile(input_path):
            # If input_path is a video file.
            if (input_path.endswith(('mp4', 'mkv', 'avi', 'flv', 'mov'))):
                video_list = [
                    {
                        'basename' : os.path.basename(input_path),
                        'dirname' : os.path.split(input_path)[0],
                        'format' : os.path.splitext(os.path.basename(input_path))[1],
                        'abspath' : input_path
                    }
                ]
        
        else:
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
        
class VideoMerger(VideoManager):
    """
    Merge video in the target folder.
    """
    
    class EncoderIndex(Enum):
        libx264 = auto()
        libx265 = auto()
#        libsvtav1 = auto()
    
    FILELIST_TXT_PATH = ''
    ENCODER_DICT = {
        f'{EncoderIndex.libx264.value}' : 'libx264',
        f'{EncoderIndex.libx265.value}' : 'libx265',
#        f'{EncoderIndex.libsvtav1.value}' : 'libsvtav1',
    }
    
    def __init__(self, input_path, install_path):
        super().__init__(input_path, install_path)
        self.FILELIST_TXT_PATH = self.get_filelist_txt_path()
        
    def get_filelist_txt_path(self):
        """
        """
        for root, dir, file in os.walk(self.INSTALL_PATH):
            if 'filelist.txt' in file:
                return os.path.join(root, 'filelist.txt')                
    
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
                
        # print("# filelist.txt: ")
        # print(filelist_txt.read())
        filelist_txt.close()
        
    def merge_files(self, output_path=None):
        """ 
        Merge the files in the filelist.txt to the output.mp4.
        
        Args:
            `input_path`: the path of the folder which contain the videos to merge.
            `output_path`: the path of the output.mp4.
        """
        if (output_path == None):
            output_path = os.path.join(self.INPUT_PATH, "output.mp4")
        
        self.get_filelist_txt()
        command = [
            self.FFMPEG_PATH,
            '-hide_banner',
            '-f', 'concat',
            '-safe', '0', 
            '-i', self.FILELIST_TXT_PATH,
        #    '-c', 'copy',
        #    output_path
        ]
        
        if input('Wether you want to copy the videos (y/n): ').lower() in ('y', ''):
            print('Encoder: copy')
            command.append('-c')
            command.append('copy')
        else:
            while True:
                print(self.ENCODER_DICT)
                command.append('-c:v')
                encoder = input('Please select the encoder: ')
                if encoder in self.ENCODER_DICT:
                    command.append(self.ENCODER_DICT[encoder])
                    break
                elif encoder == '':
                    command.append(self.ENCODER_DICT['1'])
                    break
                else:
                    print('Input param does not exist!')
        
        command.append(output_path)
        try:
            subprocess.run(command, check=True)
        
        except subprocess.CalledProcessError as e:
            print(f'ffmpeg process error! output:{e.returncode}')
            return -1
            
        return 0
            
class ThumbGenerator(VideoManager):
    """
    """
    CURRENT_PATH = ''
    
    def __init__(self, input_path, install_path):
        super().__init__(input_path, install_path)
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
                subprocess.run(command, check=True)
            
            except subprocess.CalledProcessError as e:
                print(f'ffmpeg process error: {e.returncode}')
                
        return
            
class FormatTransformer(VideoManager):
    """
    """
    OUTPUT_FORMAT = ''
    VALID_OUTPUT_FORMAT_TUPLE = ('mp4', 'mkv', 'avi', 'mov', 'flv')
    
    def __init__(self, input_path, output_format, install_path):
        super().__init__(input_path, install_path)
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
                    
                output_path = os.path.join(video['dirname'], os.path.splitext(video['basename'])[0]) + f'.{output_format}'
                command.append(output_path)
                
                try:
                    subprocess.run(command, check=True)
                    
                except subprocess.CalledProcessError as e:
                    print(f'{e.returncode}')
                    return -1
            
class VideoSpilter(VideoManager):
    """
    """
    def __init__(self, input_path, install_path):
        super().__init__(input_path, install_path)
        
    def video_spilt(self, spilt_size):
        
        for video in self.VIDEO_LIST:
            
            # Get video & audio bitrate.
            command = [
                self.FFPROBE_PATH,
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=bit_rate',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video['abspath']
            ]
            
            video_bitrate = subprocess.check_output(command).strip().decode('utf-8')
            # print(video_bitrate)
            
            command = [
                self.FFPROBE_PATH,
                '-v', 'error',
                '-select_streams', 'a:0',
                '-show_entries', 'stream=bit_rate',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video['abspath']
            ]
            
            audio_bitrate = subprocess.check_output(command).strip().decode('utf-8')
            # print(audio_bitrate)
            
            video_size_persec = (int(video_bitrate) + int(audio_bitrate)) / 8
            spilt_time = int((int(spilt_size) * 1000 * 1000) / (video_size_persec))
            
            output_path = os.path.join(video['dirname'], os.path.splitext(video['basename'])[0])
            if not os.path.exists(output_path):
                os.mkdir(output_path)
                
            output_path = os.path.join(output_path, 'output%02d.mp4')
            
            command = [
                self.FFMPEG_PATH,
                '-i', video['abspath'],
                '-c', 'copy',
                '-f', 'segment', '-segment_time', f'{spilt_time}',
                '-reset_timestamps', '1',
                output_path
            ]
            
            try:
                subprocess.run(command, check=True)
                
            except subprocess.CalledProcessError as e:
                print(f'Video spilt failed! Return code: {e.returncode}')
                return -1
            
        return