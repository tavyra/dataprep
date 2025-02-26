import os
import subprocess
import shutil
import imageio
from PIL import Image

def get_webm_dimensions(webm_file):
    reader = imageio.get_reader(webm_file)
    for im in reader:
        return im.shape[:2][::1]
    return None

def get_gif_dimensions(gif_file):
    with Image.open(gif_file) as im:
        return im.size

def resize_and_crop_video(input_path, output_path, dimensions):
    width, height = dimensions
    video_aspect_ratio = width / height
    scale_factor = max(width / video_aspect_ratio, height)
    scaled_width = int(scale_factor * video_aspect_ratio)
    scaled_height = int(scale_factor)

    filter_string = f"scale={scaled_width}:{scaled_height},crop={width}:{height}"
    cmd = ["ffmpeg", "-v", "error", "-i", input_path, "-crf", "17", "-vf", filter_string, "-c:a", "copy", output_path]
    subprocess.run(cmd)

def closest_dimensions(target_dimensions, current_dimensions):
    current_width, current_height = current_dimensions
    closest = None
    min_diff = float('inf')
    for width, height in target_dimensions:
        diff = abs(current_width / current_height - width / height)
        if diff < min_diff and width <= current_width and height <= current_height:
            min_diff = diff
            closest = (width, height)
    return closest

def convert_to_x264_mp4(input_folder, output_folder, target_dimensions, secondary_dimensions=None, tertiary_dimensions=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    rejects_folder = os.path.join(output_folder, 'small')
    if not os.path.exists(rejects_folder):
        os.makedirs(rejects_folder)
    error_folder = os.path.join(output_folder, 'error')
    if not os.path.exists(error_folder):
        os.makedirs(error_folder)

    supported_extensions = ['.gif', '.webm']

    for filename in os.listdir(input_folder):
        if any(filename.lower().endswith(ext) for ext in supported_extensions):
            input_file = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '.mp4'
            output_file = os.path.join(output_folder, output_filename)

            probe_cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {input_file}"
            result = subprocess.run(probe_cmd, shell=True, capture_output=True, text=True)

            if result.stdout.strip() == '':
                if input_file.lower().endswith('.gif'):
                    current_dimensions = get_gif_dimensions(input_file)
                elif input_file.lower().endswith('.webm'):
                    current_dimensions = get_webm_dimensions(input_file)
                else:
                    reject_file = os.path.join(error_folder, filename)
                    shutil.copy(input_file, reject_file)
                    print(f"Rejected {filename} as ffprobe failed to get dimensions.")
                    continue
            else:
                current_dimensions = tuple(map(int, result.stdout.strip().split('x')))

            target_dimensions_tuple = closest_dimensions(target_dimensions, current_dimensions)
            primary_target_dimensions = target_dimensions_tuple

            if secondary_dimensions is not None:
                secondary_target_dimensions = closest_dimensions(secondary_dimensions, current_dimensions)
            else:
                secondary_target_dimensions = None
            if tertiary_dimensions is not None:
                tertiary_target_dimensions = closest_dimensions(tertiary_dimensions, current_dimensions)
            else:
                tertiary_target_dimensions = None

            if primary_target_dimensions is None:
                if secondary_target_dimensions is None:
                    if tertiary_target_dimensions is None:
                        reject_file = os.path.join(rejects_folder, filename)
                        shutil.copy(input_file, reject_file)
                        print(f"Rejected {filename} as it cannot be downscaled to any of the target dimensions.")
                        continue
                    else:
                        target_dimensions_tuple = tertiary_target_dimensions
                else:
                    target_dimensions_tuple = secondary_target_dimensions
            else:
                target_dimensions_tuple = primary_target_dimensions


            resize_and_crop_video(input_file, output_file, target_dimensions_tuple)

            print(f"Converted {filename} to {output_filename} with target dimensions {target_dimensions_tuple[0]}x{target_dimensions_tuple[1]}")

input_folder = '/home/path/to/images'
output_folder = '/home/path/to/folder'
first_dimensions = [(2400, 960), (960, 2400), (2160, 1080), (1080, 2160), (1920, 1080), (1080, 1920), (1920, 1440), (1440, 1920), (1440, 2160), (2160, 1440), (2160, 2160)]
second_dimensions = [(1800, 720), (720, 1800), (1440, 720), (720, 1440), (1280, 720), (720, 1280), (1280, 960), (960, 1280), (1440, 960), (960, 1440), (1280, 1280)]
third_dimensions = [(1200, 480), (480, 1200), (960, 480), (480, 960), (864, 480), (480, 864), (960, 720), (720, 960), (960, 640), (640, 960), (960, 960)]
#target_dimensions = [(640, 256), (256, 640), (720, 360), (360, 720), (576, 320), (320, 576), (640, 480), (480, 640), (720, 480), (480, 720), (480, 480)]
#target_dimensions = [(480, 240), (240, 480), (448, 256), (256, 448), (480, 368), (368, 480), (384, 288), (288, 384), (360, 360)]
convert_to_x264_mp4(input_folder, output_folder, first_dimensions, second_dimensions, third_dimensions)
