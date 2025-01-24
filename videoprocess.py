import os
import random
import json
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip

def attach_tts_to_videos():
    """
    Attaches TTS audio clips from a user-specified folder to videos in another folder, 
    selecting random time slots that match the TTS audio length. Updates metadata with associated links.
    """

    # Get the directory of TTS audio files
    folder_name = input("Enter the name of the folder: ").strip()
    tts_folder = f"{os.path.dirname(os.path.abspath(__file__))}/{folder_name}"

    tts_folder = input("Enter the folder path containing TTS audio files: ").strip()
    if not os.path.exists(tts_folder):
        print(f"Error: The folder '{tts_folder}' does not exist.")
        return

    # Get the directory of videos
    videos_folder = input("Enter the folder path containing video files: ").strip()
    if not os.path.exists(videos_folder):
        print(f"Error: The folder '{videos_folder}' does not exist.")
        return

    # Create metadata dictionary to store TTS link and its video position
    metadata = {}

    # Iterate over all video files in the videos folder
    video_files = [f for f in os.listdir(videos_folder) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
    if not video_files:
        print(f"No video files found in '{videos_folder}'.")
        return

    # Iterate over each video file
    for video_file in video_files:
        video_path = os.path.join(videos_folder, video_file)

        try:
            # Load the video
            video_clip = VideoFileClip(video_path)
            video_duration = video_clip.duration

            # Pick a random TTS audio file from the TTS folder
            tts_files = [f for f in os.listdir(tts_folder) if f.lower().endswith('.mp3')]
            if not tts_files:
                print(f"No TTS audio files found in '{tts_folder}'.")
                return

            tts_file = random.choice(tts_files)
            tts_path = os.path.join(tts_folder, tts_file)

            # Load the TTS audio and get its duration
            tts_clip = AudioFileClip(tts_path)
            tts_duration = tts_clip.duration

            # Select a random time slot in the video where the TTS audio can fit
            max_start_time = video_duration - tts_duration
            if max_start_time <= 0:
                print(f"Skipping '{video_file}' because it is too short for the TTS audio.")
                continue

            random_start_time = random.uniform(0, max_start_time)

            # Add the TTS audio to the video at the selected time slot
            composite_audio = CompositeVideoClip([video_clip.set_audio(tts_clip.set_start(random_start_time))])
            output_video_path = os.path.join(videos_folder, f"output_{video_file}")
            composite_audio.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
            print(f"TTS audio added to '{video_file}' at {random_start_time:.2f} seconds.")

            # Add metadata
            metadata[output_video_path] = {
                "tts_file": tts_file,
                "start_time": random_start_time,
                "tts_duration": tts_duration,
                "link": f"https://example.com/link/{tts_file}"  # Placeholder for the actual link
            }

        except Exception as e:
            print(f"Error processing '{video_file}': {e}")

    # Save metadata to a JSON file
    metadata_path = os.path.join(videos_folder, "metadata.json")
    with open(metadata_path, 'w') as meta_file:
        json.dump(metadata, meta_file, indent=4)
    print(f"Metadata saved to '{metadata_path}'.")

    print("Process completed.")

