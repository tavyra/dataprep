import os
import subprocess

def process_directory(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.mp4'):
                file_path = os.path.join(root, file)
                output_dir = os.path.join(root, 'processed')
                os.makedirs(output_dir, exist_ok=True)
                
                video_output = os.path.join(output_dir, os.path.splitext(file)[0] + '.mp4')
                audio_output = os.path.join(output_dir, os.path.splitext(file)[0] + '.mp3')
                
                command_video = ['ffmpeg', '-i', file_path, '-c:v', 'copy', '-an', video_output]
                command_audio = ['ffmpeg', '-i', file_path, '-c:a', 'copy', '-vn', audio_output]
                
                subprocess.run(command_video)
                subprocess.run(command_audio)

process_directory('path/to/folder')
