import subprocess
import pandas as pd

def detect_silent_sections(input_file, output_csv):
    # Command to detect silence using FFmpeg
    command = [
        'ffmpeg', '-i', input_file, 
        '-af', 'silencedetect=n=-30dB:d=1',
        '-f', 'null', '-']
    
    # Run the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    # Parse the output to find silent sections
    silent_data = []
    for line in result.stdout.decode().splitlines():
        if 'silence_start' in line:
            parts = line.split(' ')
            try:
                start_time = float(parts[2].replace('silence_start:', ''))
                end_time = float(parts[3].replace('silence_end:', ''))
                silent_data.append([start_time, end_time])
            except ValueError:
                continue  # Skip lines that don't contain valid times
        elif 'silence_end' in line:
            parts = line.split(' ')
            try:
                end_time = float(parts[2].replace('silence_end:', ''))
                silent_data[-1][1] = end_time  # Update the last entry's end time
            except ValueError:
                continue  # Skip lines that don't contain valid times
    
    # Save to CSV
    df = pd.DataFrame(silent_data, columns=['Start Time', 'End Time'])
    df.to_csv(output_csv, index=False)

# Usage
input_wav_file = 'file.wav'
output_csv_file = 'file.csv' # save .csv for operations or future use
detect_silent_sections(input_wav_file, output_csv_file)
