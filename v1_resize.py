import os
import subprocess

def check_and_resize(directory, x, y):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp4'):
                filepath = os.path.join(root, file)
                result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', filepath], stdout=subprocess.PIPE)
                width, height = map(int, result.stdout.decode().split(','))
                
                if width > y and height > x:
                    new_size = f"'{x}:{y}'" if width > height else f"'{y}:{x}'"
                    subprocess.run(['ffmpeg', '-i', filepath, '-vf', f'scale={new_size}', os.path.join(root, f'resized_{file}')])

# Replace 'your_directory_path' with the path to your directory containing the videos
check_and_resize('path/to/folder', 720, 480)
