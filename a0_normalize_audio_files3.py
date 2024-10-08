import os
import subprocess
import shutil

def check_file_length(source_file):
    command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', source_file]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        return False
    duration = float(result.stdout.decode('utf-8').strip())
    return duration

def normalize_and_convert(input_dir, output_dir, reject_dir, target_level=-16):
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith(".flac"):
                input_file = os.path.join(root, filename)
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                reject_subdir = os.path.join(reject_dir, relative_path)
                output_file = os.path.join(output_subdir, os.path.splitext(filename)[0] + ".wav")
                output_alt = os.path.join(output_subdir, os.path.splitext(filename)[0] + ".flac")
                reject_file = os.path.join(reject_subdir, os.path.splitext(filename)[0] + ".wav")
                duration = check_file_length(input_file)
                if duration !=0:    
                    if not os.path.exists(output_subdir):
                        os.makedirs(output_subdir)
                    #if duration <3:
                    #    pass
                    #    #command = ["ffmpeg-normalize", input_file, output_alt]
                    #else:
                    command = [
                        "ffmpeg",
                        "-i", input_file,
                        "-filter_complex", f"loudnorm=I=-20:TP=-3:LRA=18",  
                        "-ar", "44100",                  # Set the sample rate to 44100 Hz
                        "-f", "wav",                     # Output format as WAV
                        output_file
                        ]            
                    subprocess.run(command)
                else: print("now you fucked up")
                    #if not os.path.exists(reject_subdir):
                    #    os.makedirs(reject_subdir)
                    #shutil.copy2(input_file, reject_file)
                    
input_directory = "path/to/audio_files"
output_directory = "path/to/save"
reject_directory = "path/for/problematic_files" #probably not needed
normalize_and_convert(input_directory, output_directory, reject_directory)
