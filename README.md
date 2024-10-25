# dataprep
Set of tools to process videos into a/v datasets. This is a work in progress, but jsons saved will be usable by future uploads

These scripts assume you have FFMPEG installed to your system PATH. Use batch_demux to split long videos into .mp4 and .wav

The A scripts are to process the audio and V scripts for images. Normalize as often as you like, particularly before silence detection. Desilence removes sections of silence based on threshold. Slice then splits the audio into manageable chunks to add labels. If adjusting thresholds/lengths, check an output file to make sure it isn't cutting while there is noise.

For video, there is a step missing between resize, which makes a copy of the video with a prefix resized_ at the desired resolution for training, and split_vlm_png, which goes through a folder of videos and extracts frames at the specified locations (default: 3 images, 1 near each end and 1 in center). This is an active area of development.

You may also use EasyAnimate for large datasets and simply copy the data folder after processing to your dektop if you prefer to not wait.

The data labelling tools are used to quickly create datasets with relevant information. Currently, there is an image captioning tool, a video captioning tool which loads a folder of images sliced from a video (created after slicing with VLM script), a character:emotion labelling tool for images/videos, a character:emotion labelling tool for SHORT audio clips (simple GUI, plays full clip), and a tool you may adapt for training purposes (it currently holds counts for species, anthro type and checkboxes for object detection)
![Audio Captioner](https://github.com/tavyra/dataprep/blob/main/audio_captioning.png)
![Data Labelling](https://github.com/tavyra/dataprep/blob/main/data_labelling.png)
![Emotion Labelling](https://github.com/tavyra/dataprep/blob/main/emotion_labelling.png)
![Image Captioner](https://github.com/tavyra/dataprep/blob/main/VLM_caption.png)
