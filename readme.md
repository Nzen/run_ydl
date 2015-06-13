## youtube_dl utilities

[Youtube_dl](http://rg3.github.io/youtube-dl/download.html) is a great program to harvest videos from video hosting sites. I leave whether harvesting (il)licitly uploaded videos from hosting sites is great to your discretion. In my case, though, I wanted to have more control over how it batched or postprocessed files.

### run_yd

takes a text file with flags that correspond to youtube, yt playlist, bandcamp, etc and downloads each one via youtube_dl. Expects a filename argument

### ff_run

Renames the files in this folder to strip extra hyphens and stuff. Tells ffmpeg to convert them to mp3 into a folder called 'done'.

### License

WTFPL as described on [its site](www.wtfpl.net). This is just a little string manipulation. I can hardly pretend to feel offended if you don't credit me or whatever. youtube_dl is public domain. ffmpeg is gpl. But, I don't actually bundle them in this software, so no worries.