from pydub import AudioSegment
import os
def split_audio(input_folder, output_folder, min_chunk_length=15000):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Define the silence threshold in milliseconds
    silence_threshold = -68  # 60 dB
    # Iterate over all .wav files in the input folder
    for file_name in os.listdir(input_folder):
        # enabling .mp3 will reduce speed as it needs to convert to wav first
        #if file_name.endswith(".wav") or file_name.endswith(".mp3"):
        if file_name.endswith(".wav"):
            file_path = os.path.join(input_folder, file_name)
            audio = AudioSegment.from_wav(file_path)
            # Initialize variables
            current_chunk = AudioSegment.silent(duration=0)
            current_chunk_length = 0
            chunk_index = 1
            # Iterate over the audio segments
            for i in range(len(audio)):
                sample = audio[i]
                if sample.dBFS < silence_threshold:
                    if current_chunk_length + len(sample) >= min_chunk_length:
                        # Save the current chunk
                        output_name, extension = file_name.rsplit('.',1)
                        output_file = os.path.join(output_folder, f"{output_name}_part_{chunk_index:03d}.wav")
                        current_chunk.export(output_file, format="wav")

                        print(f"Chunk {chunk_index} saved: {output_file}")
                        # Reset the current chunk and length
                        current_chunk = AudioSegment.silent(duration=0)
                        current_chunk_length = 0
                        chunk_index += 1
                    # Add the sample to the current chunk
                    current_chunk += sample
                    current_chunk_length += len(sample)
                else:
                    # Add the sample to the current chunk
                    current_chunk += sample
                    current_chunk_length += len(sample)
            # Save the last chunk if it exists
            if current_chunk:
                output_name, extension = file_name.rsplit('.',1)
                output_file = os.path.join(output_folder, f"{output_name}_part_{chunk_index:03d}.wav")
                current_chunk.export(output_file, format="wav")
                print(f"Chunk {chunk_index} saved: {output_file}")
        else:
            pass
if __name__ == "__main__":
    root_dir = "path/to/folder"
    target_dir = "path/to/save"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for item in os.listdir(root_dir):
        input_folder = os.path.join(root_dir, item)
        if os.path.isdir(input_folder):
            output_folder = os.path.join(target_dir, item)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            split_audio(input_folder, output_folder)
