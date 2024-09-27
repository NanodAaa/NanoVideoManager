import subprocess

# 定义 FFmpeg 命令
command = [
    'a:\\NanodAaa\\NanoVideoManager\\NanoVideoManager\\ffmpeg\\bin\\ffmpeg.exe',
    '-i', r'E:\NanodAaa\VIDEO\OBS_OUTPUT\0112 DVR6\2024-01-12 15-10-03.mp4',
    '-fs', '1G',  # 尝试设置为较小的值
    '-c', 'copy',
    'E:\\NanodAaa\\VIDEO\\OBS_OUTPUT\\0112 DVR6\\2024-01-12 15-10-03\\output%03d.mp4'
]

# 执行命令
try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f'FFmpeg process error! Output: {e.returncode}')