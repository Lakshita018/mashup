Mashup Generator

Audio mashup tool that downloads YouTube videos, trims audio clips, and merges them into a single MP3 file.

This project contains:

Program 1 – Command Line Version

Program 2 – Web Application (Deployed on Vercel)

Program 1 – Command Line

Generates mashup using terminal.

Usage
python 102303505.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>

Example
python 102303505.py "Sharry Maan" 20 30 102303505-output.mp3

Sample Output

![CLI Output](cli-output.png)

Conditions

NumberOfVideos > 10

AudioDuration > 20 seconds

Output file must end with .mp3

Install
pip install yt-dlp pydub ffmpeg-python audioop-lts
pip install ffmpeg-downloader
python -m ffmpeg_downloader install

Program 2 – Web Application

Web-based mashup generator with email delivery.

Live Demo:
https://mashup-working.vercel.app/

Web Interface

![Mashup Web Application](mashup-website.png)

User Inputs

Singer Name

Number of Videos (>10)

Duration (>20 sec)

Email ID

Output is sent as a ZIP file via email.

Project Structure
mashup/
├── program-1/
│   └── 102303505.py
├── program-2/
│   ├── index.html
│   ├── api/
│   ├── requirements.txt
│   └── vercel.json
└── README.md

Workflow

Download YouTube videos

Extract audio

Trim clips

Merge into one MP3

Deliver (local save / email)

Author
Lakshita Gupta
Roll No: 102303505