import os
import csv
import subprocess
import numpy as np
from pydub import AudioSegment

# recommended settings: pass1: threshold -30, min length 1000 pass2: threshold -40, min length 400
# FYI, the filter width is 200ms going lower can cut audio in undesireable locations

def find_silence(input_file, output_csv, threshold=-30.0, min_silence_len=2000):
    # Command to use ffmpeg to detect silence
    seconds_silence = min_silence_len / 1000
    command = [
        'ffmpeg', '-i', input_file,
        '-af', f'silencedetect=noise={threshold}dB:duration={seconds_silence}',
        '-f', 'null', '-',
    ]

    # Run the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {result.stderr.decode('utf-8')}")

    # Parse the output to find silence periods
    silence_info = []
    for line in result.stderr.decode('utf-8').split('\n'):
        if 'silence_start' in line:
            parts = line.split(': ')
            start = float(parts[1])
            print("start ", start)
        if 'silence_end' in line:
            parts = line.split(': ')
            parts = parts[1].split(' ')
            end = float(parts[0])
            print("end ", end)
            silence_info.append((start, end))

    # Save to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Start', 'End'])
        writer.writerows(silence_info)

    return silence_info

def trim_silence(input_file, output_file, silence_info):
    # Calculate the start and end times for trimming
    start_times = [info[0] for info in silence_info]
    end_times = [info[1] for info in silence_info]

    # Load the audio file
    audio = AudioSegment.from_wav(input_file)
    total_duration = len(audio)

    # Create a new audio segment excluding the silent parts
    trimmed_audio = AudioSegment.silent(duration=0)
    last_end = 0
    for start, end in silence_info:
        start_ms = int(start * 1000)
        end_ms = int(end * 1000)
        trimmed_audio += audio[last_end:start_ms]
        last_end = end_ms
    trimmed_audio += audio[last_end:]

    # Export the trimmed audio
    trimmed_audio.export(output_file, format='wav')

# Example usage
input_folder = 'path/to/folder'
output_folder = 'path/to/save'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


for filename in os.listdir(input_folder):
    if filename.endswith('.wav'):
        input_file = os.path.join(input_folder, filename)
        output_csv = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")
        output_trimmed_file = os.path.join(output_folder, f"trimmed_{filename}")

        silence_info = find_silence(input_file, output_csv)
        trim_silence(input_file, output_trimmed_file, silence_info)
