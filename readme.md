## youtube_dl utilities

[Youtube_dl](http://rg3.github.io/youtube-dl/download.html) is a great program to harvest videos from video hosting sites. I leave whether 'harvesting (il)licitly uploaded videos from hosting sites is great' to your discretion. I wanted to have more control over how it batched or postprocessed files. Assumes python 3 ; frozen python 2.7 versions in the py2 folder

### run_yd

Takes a text file with flags that correspond to youtube, yt playlist, bandcamp, etc and downloads each one via youtube_dl. Expects a filename argument. 0.txt has examples of flags. Saves mp4 preferentially, change in output{} to suit you.

    python3 run_yd.py 0.txt

### ff_run

Renames the files in this folder to strip extra hyphens and stuff. Tells [ffmpeg](https://www.ffmpeg.org/) to convert them to mp3 into a folder called 'done'. Expects how many to process before pausing (to keep the heat down). That last bit doesn't seem to work with linux-mint :\

    python3 ff_run.py 30

### remove_playlist

Recopies the lines of the specified file without text between an ampersand and a tab. Ignores an ampersand in the first position and uses the end of line when the line lacks a tab. Writes the new file with the prefix 'new_'. Not inclined to bundle this with run_ydl, for historical and other reasons.

    python3 remove_playlist.py 0.txt

### clean_ryd

Deprecated tool for renaming files.

### License

WTFPL as described on [its site](www.wtfpl.net). This is just a little string manipulation. I can hardly pretend to feel offended if you don't credit me or whatever. youtube_dl is public domain. ffmpeg and avconv are gpl. But, I don't actually bundle them in this software, so no worries. (I'd have to put them in your PATH if I did.)
