import os
import ffmpeg
import subprocess

def resize_videos(directory, destination):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp4'):
                file_path = os.path.join(root, file)
                video = ffmpeg.probe(file_path)
                width = int(video['streams'][0]['width'])
                height = int(video['streams'][0]['height'])

                if width > 720 or height > 480:
                    new_width = width
                    new_height = height

                    if width > 720:
                        new_width = 720
                        new_height = int((720 / width) * height)
                        new_height = (new_height // 2) * 2

                    if new_height < 480:
                        new_height = 480
                        new_width = int((480 / height) * width)
                        new_width = (new_width // 2) * 2

                    output_path = os.path.join(destination, f"{file}")
                    command = [
                        'ffmpeg',
                        '-i', file_path,  # Input file
                        '-filter:v', f'scale={new_width}:{new_height}',
                        '-y',  # Automatically answer 'yes' to overwrite prompts
                        output_path  # Output file
                    ]
                    subprocess.run(command)
                    print(f"Resized {file_path} to {output_path}")

root_directory = 'path/to/folder'
output_directory = 'path/to/save'

resize_videos(root_directory, output_directory)
