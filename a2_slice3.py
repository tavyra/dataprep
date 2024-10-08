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
                        output_file = os.path.join(output_folder, f"{file_name}_part_{chunk_index}.wav")
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
                output_file = os.path.join(output_folder, f"{file_name}_part_{chunk_index}.wav")
                current_chunk.export(output_file, format="wav")

                print(f"Chunk {chunk_index} saved: {output_file}")
if __name__ == "__main__":
    input_folder = "path/to/trimmed_files"
    output_folder = "path/to/save"
    split_audio(input_folder, output_folder)
