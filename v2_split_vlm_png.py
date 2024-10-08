import os
import ffmpeg
import moviepy.editor as mp

def extract_frames(video_path, output_folder):
    # Open the video file
    video = mp.VideoFileClip(video_path)

    # Get the duration of the video
    duration = video.duration

    # Calculate the times for the frames to extract
    frame_times = [0.04 * duration, 0.5 * duration, 0.96 * duration]

    # Extract frames at specified times
    for i, frame_time in enumerate(frame_times):
        frame = video.get_frame(frame_time)
        output_path = os.path.join(output_folder, f'{i+1}.png')
        mp.ImageClip(frame).save_frame(output_path, t=frame_time)

def main(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all .mp4 files in the input folder
    for index, file in enumerate(os.listdir(input_folder)):
        if file.endswith('.mp4'):
            index_group = os.path.join(output_folder, f'{index}')
            if not os.path.exists(index_group):
                os.makedirs(index_group)
            video_path = os.path.join(input_folder, file)
            extract_frames(video_path, index_group)


if __name__ == "__main__":
    input_folder = 'path/to/input'  # Change this to your input folder path
    output_folder = 'path/to/Processed'  # Change this to your output folder path
    main(input_folder, output_folder)
