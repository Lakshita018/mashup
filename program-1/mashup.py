import sys
import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def main():
    # -------------------------
    # CHECK ARGUMENTS
    # -------------------------
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]
    
    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("Error: NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    output_file = sys.argv[4]

    if num_videos <= 10:
        print("Error: NumberOfVideos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("Error: AudioDuration must be greater than 20 seconds.")
        sys.exit(1)

    print("Downloading videos...")

    # -------------------------
    # DOWNLOAD VIDEOS
    # -------------------------
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
    }

    os.makedirs("downloads", exist_ok=True)

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch{num_videos}:{singer} songs"])

    print("Download complete.")

    # -------------------------
    # PROCESS AUDIO
    # -------------------------
    merged_audio = AudioSegment.empty()

    for file in os.listdir("downloads"):
        if file.endswith(".webm") or file.endswith(".m4a"):
            file_path = os.path.join("downloads", file)

            try:
                audio = AudioSegment.from_file(file_path)
                cut_audio = audio[:duration * 1000]  # milliseconds
                merged_audio += cut_audio
            except Exception as e:
                print("Error processing file:", file, e)

    # -------------------------
    # EXPORT FINAL FILE
    # -------------------------
    try:
        merged_audio.export(output_file, format="mp3")
        print("Mashup created successfully:", output_file)
    except Exception as e:
        print("Error exporting file:", e)


if __name__ == "__main__":
    main()
