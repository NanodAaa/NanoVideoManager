import os
import subprocess
from enum import Enum, auto

class VideoManager:
    """
    """
    class EncoderIndex(Enum):
        libx264 = auto()
        libx265 = auto()
        h264_nvenc = auto()
        hevc_nvenc = auto()
        h264_amf = auto()
        hevc_amf = auto()
        h264_vaapi = auto()
#        libsvtav1 = auto()

    ENCODER_DICT = {
        f'{EncoderIndex.libx264.value}' : 'libx264',
        f'{EncoderIndex.libx265.value}' : 'libx265',
        f'{EncoderIndex.h264_nvenc.value}' : 'h264_nvenc',
        f'{EncoderIndex.hevc_nvenc.value}' : 'hevc_nvenc',
        f'{EncoderIndex.h264_amf.value}' : 'h264_amf',
        f'{EncoderIndex.hevc_amf.value}' : 'hevc_amf',
        f'{EncoderIndex.h264_vaapi.value}' : 'h264_vaapi',
#        f'{EncoderIndex.libsvtav1.value}' : 'libsvtav1',
    }
    
    class FormatIndex(Enum):
        mp4 = auto()
        mkv = auto()
        flv = auto()
        avi = auto()
        mov = auto()
    
    FORMAT_DICT = {
        f'{FormatIndex.mp4.value}' : '.mp4',
        f'{FormatIndex.mkv.value}' : '.mkv',
        f'{FormatIndex.flv.value}' : '.flv',
        f'{FormatIndex.avi.value}' : '.avi',
        f'{FormatIndex.mov.value}' : '.mov',
    }
    
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
    
    def get_video_bitrate(self, input_path):
        """
        Get video bitrate.
        """
        command = [
                self.FFPROBE_PATH,
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=bit_rate',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                input_path,
            ]   
        video_bitrate = subprocess.check_output(command).strip().decode('utf-8')
        return video_bitrate
    
    def get_audio_bitrate(self, input_path):
        """
        Get audio bitrate.
        """
        command = [
                self.FFPROBE_PATH,
                '-v', 'error',
                '-select_streams', 'a:0',
                '-show_entries', 'stream=bit_rate',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                input_path,
            ]
        audio_bitrate = subprocess.check_output(command).strip().decode('utf-8')
        return audio_bitrate
    
    def get_video_duration(self, input_path):
        """
        Get video duration.
        
        Args:
            `input_path`: File to get duration.
            
        Returns:
            `video_duration`: Video duration.
        """
        command =  [
            self.FFPROBE_PATH,
            "-v", "error",
            "-select_streams", "v:0", 
            "-show_entries", "format=duration", 
            "-of", "default=noprint_wrappers=1:nokey=1", 
            input_path
        ]
        
        video_duration = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        return float(video_duration.stdout)
    
    def get_video_info(self, input_path):
        VideoInfoDict = {
            'video-duration' : self.get_video_duration(input_path),
            'video-bitrate' : self.get_video_bitrate(input_path),
            'audio-bitrate' : self.get_audio_bitrate(input_path),
        }
        
        return VideoInfoDict
        
class VideoMerger(VideoManager):
    """
    Merge video in the target folder.
    """
    FILELIST_TXT_PATH = ''
    
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
        
        while True:
            print(self.ENCODER_DICT)
            encoder = input('Please select the encoder (Empty=copy): ')
            if encoder in self.ENCODER_DICT:
                command.append('-c:v')
                command.append(self.ENCODER_DICT[encoder])
                break
            elif encoder == '':
                command.append('-c')
                command.append('copy')
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
    class AlgorithmIndex(Enum):
        most_meaningful = auto()
        avg_frametime = auto()
        
    GENERATE_ALGORITHM_DICT = {
        'most-meaningful' : f'{AlgorithmIndex.most_meaningful.value}',
        'avg-frametime' : f'{AlgorithmIndex.avg_frametime.value}',
    }
    
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
        
        print(self.GENERATE_ALGORITHM_DICT)
        generate_algorithm = input('Please select the algorithm of generation: ')
        thumb_total_nums = int(input('Please input the number of thumbs to generate: '))
        for video in self.VIDEO_LIST:
            output_path = os.path.join(video['dirname'], os.path.splitext(video['basename'])[0])
            if (os.path.exists(output_path) == False):
                os.mkdir(output_path)
                
            if generate_algorithm == self.GENERATE_ALGORITHM_DICT['most-meaningful']:
                """
                Most-meaningful algorithm.
                
                By d33pika. Asked Jan 18, 2013 at 8:35
                https://superuser.com/questions/538112/meaningful-thumbnails-for-a-video-using-ffmpeg
                """
                output_path = os.path.join(output_path, 'out%02d.jpg')
                command = [self.FFMPEG_PATH, 
                                '-y',
                                '-ss', '3',
                                '-i', video['abspath'], 
                                '-vf', 'select=gt(scene\,0.4)',
                                '-frames:v', '20', 
                                '-fps_mode', 'vfr',
                                output_path] 
                
                result = subprocess.run(command, check=False)
                if result.returncode != 0:
                    print(f"Error processing {video['abspath']}. Skipping to next file.")
                                
            elif generate_algorithm == self.GENERATE_ALGORITHM_DICT['avg-frametime']:                                       
                """
                Avg frame time algorithm.
                
                Pseudo-code
                for X in 1..N
                T = integer( (X - 0.5) * D / N )  
                run `ffmpeg -ss <T> -i <movie>
                            -vf select="eq(pict_type\,I)" -vframes 1 image<X>.jpg`
                
                T - time point for tumbnail
                
                By gertas. Answered Oct 6, 2014 at 20:21. 
                https://superuser.com/questions/538112/meaningful-thumbnails-for-a-video-using-ffmpeg
                """
                video_duration = self.get_video_duration(video['abspath'])
                for X in range(1, thumb_total_nums + 1):
                    output_path_num = os.path.join(output_path, f'output{X-1}.jpg')
                    T = int((X - 0.5) * video_duration / thumb_total_nums)
                    command = [
                        self.FFMPEG_PATH,
                        '-y',
                        '-ss', f'{T}',
                        '-i', video['abspath'],
                        '-vf', 'select=eq(pict_type\,I)',
                        '-vframes', '1',
                        output_path_num
                    ]
                    
                    result = subprocess.run(command, check=False)
                    if result.returncode != 0:
                        print(f"Error processing {video['abspath']}. Skipping to next file.")
            
            else:
                print('Algorithm does not exists!')
                return -1
                
        return
            
class FormatTransformer(VideoManager):
    def __init__(self, input_path, install_path):
        super().__init__(input_path, install_path)
        
    def format_transform(self, input_path=None):
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
            
        while True:
            print(self.ENCODER_DICT)
            output_encoder = input('Please select a encoder(Empty == libx264): ')
            if output_encoder in self.ENCODER_DICT:
                output_encoder = self.ENCODER_DICT[output_encoder]
                break
            elif output_encoder == '':
                output_encoder = 'copy'
                break
            else:
                print('Input param error!')
                continue
            
        while True:
            print(self.FORMAT_DICT)
            output_format = input('Please select a format(Empty == .mp4): ')
            if output_format in self.FORMAT_DICT:
                output_format = self.FORMAT_DICT[output_format]
                break
            elif output_format == '':
                output_format = '.mp4'
                break
            else:
                print('Input param error!')
                continue
            
        for video in video_list:
            output_path = os.path.join(video['dirname'], os.path.splitext(video['basename'])[0]) + output_format
            command = [
                self.FFMPEG_PATH,
                '-i', video['abspath'],
                '-c:v', output_encoder,
                '-c:a', 'copy',
                output_path,
            ]
            
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