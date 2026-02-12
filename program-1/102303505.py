import sys
import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment
from pydub.utils import which

# Set FFmpeg path if installed via ffmpeg-downloader
ffmpeg_path = os.path.join(os.path.expanduser("~"), "AppData", "Local", "ffmpegio", "ffmpeg-downloader", "ffmpeg", "bin")
if os.path.exists(ffmpeg_path) and which("ffmpeg") is None:
    AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
    AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")
    os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ.get("PATH", "")


def validate_inputs(args):
    """Validate command-line arguments"""
    print("=" * 60)
    print("MASHUP GENERATOR - Validating Inputs")
    print("=" * 60)
    
    if len(args) != 5:
        print("❌ Error: Incorrect number of arguments.")
        print("Usage: python 102303505.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = args[1]
    print(f"✓ Singer Name: {singer}")

    try:
        num_videos = int(args[2])
        if num_videos <= 10:
            raise ValueError("must be greater than 10")
        print(f"✓ Number of Videos: {num_videos}")
    except ValueError as e:
        print(f"❌ Error: NumberOfVideos must be an integer greater than 10.")
        sys.exit(1)

    try:
        duration = int(args[3])
        if duration <= 20:
            raise ValueError("must be greater than 20")
        print(f"✓ Audio Duration: {duration} seconds")
    except ValueError:
        print("❌ Error: AudioDuration must be an integer greater than 20 seconds.")
        sys.exit(1)

    output_file = args[4]
    if not output_file.endswith(".mp3"):
        print("❌ Error: OutputFileName must end with .mp3")
        sys.exit(1)
    print(f"✓ Output File: {output_file}")
    print("=" * 60)

    return singer, num_videos, duration, output_file


def create_directories():
    """Create fresh directories for downloads and trimmed files"""
    print("\n📁 Preparing directories...")
    
    if os.path.exists("downloads"):
        print("   Cleaning old downloads folder...")
        shutil.rmtree("downloads")
    if os.path.exists("trimmed"):
        print("   Cleaning old trimmed folder...")
        shutil.rmtree("trimmed")

    os.makedirs("downloads")
    os.makedirs("trimmed")
    print("✓ Directories ready\n")


def download_videos(singer, num_videos):
    """Download videos from YouTube and convert to MP3"""
    print("=" * 60)
    print(f"📥 STEP 1: Downloading top {num_videos} videos of {singer}")
    print("=" * 60)

    search_query = f"ytsearch{num_videos}:{singer} official video"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,
        'noplaylist': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])
        print("\n✓ Download complete!\n")
    except Exception as e:
        print(f"\n❌ Error during download: {e}")
        sys.exit(1)


def trim_audios(duration):
    """Trim each audio file to specified duration"""
    print("=" * 60)
    print(f"✂️  STEP 2: Trimming first {duration} seconds from each audio")
    print("=" * 60)

    trimmed_files = []
    mp3_files = [f for f in os.listdir("downloads") if f.endswith(".mp3")]
    
    if not mp3_files:
        print("❌ Error: No MP3 files found in downloads folder.")
        sys.exit(1)

    total = len(mp3_files)
    print(f"Found {total} audio file(s) to process\n")

    for idx, file in enumerate(mp3_files, 1):
        file_path = os.path.join("downloads", file)
        
        try:
            print(f"[{idx}/{total}] Trimming: {file[:50]}...")
            audio = AudioSegment.from_mp3(file_path)
            trimmed_audio = audio[:duration * 1000]  # Convert to milliseconds

            output_path = os.path.join("trimmed", f"trimmed_{idx}.mp3")
            trimmed_audio.export(output_path, format="mp3")
            trimmed_files.append(output_path)
            
            print(f"        ✓ Saved to: trimmed_{idx}.mp3")

        except Exception as e:
            print(f"        ⚠️  Skipping file due to error: {e}")

    print(f"\n✓ Successfully trimmed {len(trimmed_files)} file(s)\n")
    return trimmed_files


def merge_audios(files, output_file):
    """Merge all trimmed audio files into one"""
    print("=" * 60)
    print("🎵 STEP 3: Merging audio files")
    print("=" * 60)

    if not files:
        print("❌ Error: No audio files to merge.")
        sys.exit(1)

    print(f"Merging {len(files)} audio clip(s)...\n")
    
    final_audio = AudioSegment.empty()

    for idx, file in enumerate(files, 1):
        print(f"[{idx}/{len(files)}] Adding: {os.path.basename(file)}")
        audio = AudioSegment.from_mp3(file)
        final_audio += audio

    print(f"\n📤 Exporting final mashup...")
    final_audio.export(output_file, format="mp3")
    
    total_duration = len(final_audio) / 1000
    print(f"\n✅ SUCCESS! Mashup created: {output_file}")
    print(f"📊 Total Duration: {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)")
    print("=" * 60)


def main():
    try:
        singer, num_videos, duration, output_file = validate_inputs(sys.argv)

        create_directories()
        download_videos(singer, num_videos)
        trimmed_files = trim_audios(duration)
        merge_audios(trimmed_files, output_file)

        print("\n🎉 All done! Your mashup is ready to play!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
