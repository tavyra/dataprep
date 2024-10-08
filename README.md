# dataprep
Set of tools to process videos into a/v datasets [WIP]

These scripts assume you have FFMPEG installed to your system PATH. Use batch_demux to split long videos into .mp4 and .mp3 (or wav)

The A scripts are to process the audio and V scripts for images. Normalize the audio as often as you want to keep all files roughly uniform in loudness. Desilence uses a threshold to go through a normalized audio file and cut out as much silence as possible to reduce excess data processing. Slice then splits the audio into manageable chunks to add labels. If you adjust silence ratios and especially silence lengths, check a file to make sure it is cutting the samples at appropriate places (i.e. you can only tell where the audio is cut by the time that is missing, not in the middel of dialog (though it will also trim long pauses)

For video, there is a step missing between resize, which makes a copy of the video with a prefix resized_ at the desired resolution for training, and split_vlm_png, which goes through a folder of videos and extracts frames at the specified locations (default: 3 images, 1 near each end and 1 in center).

The step you need to do yourself is cut the video into smaller scenes. I recommend using EasyAnimate for large datasets, which uses PySceneDetect and some quality metrics to filter the dataset down to more interesting samples. Simply copy the data folder after processing to your dektop and continue to the caption assistant.

Note: currently the captions are being saved to a json with the folder they come from (split_vlm makes a folder for each video to help later in displaying variable amounts of images per video)

The caption_GUI will ask for the directory containing the folders output from v2_ then asks if you have a json to load. It is expecting the loaded json to be the same format as the one it saves, so type 'no' the first time and enter a path to save an empty .json to that folder. There are NO graceful errors so be sure your paths are correct.
