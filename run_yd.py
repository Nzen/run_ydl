import os

'''
youtube-dl is great, but it doesn't seem to grab playlist arguments from a batch file.
As I don't want a whole playlist at once, this module accomodates my prefeence.

 Future:
use proper ipc to run ydl and harvest error signals, for retries

 - file format -
(&  \d+(,\d+)* | https://www.youtube.com/watch?v= | ) [\d-_\w]+

 - out to system -
youtube-dl -f 18 -o "%(upload [...] itle)s.%(ext)s" --playlist-items 6,7,8 [playlist_url]
'''

def main() :
	file = open( "1.txt" ) # or your preference, argv also possible
	playlists = file.readlines()
	file.close()
	flags = {
		'&': ['-f 18 ','yt '],
		'y' : ['-f 18 ','yt '],
		'b' : ['','bc '],
		'd' : ['-f standard ','dm'],
		'v' : ['-f h264-sd ','vi'],
		's' : ['','sc ']
	}
	for_bash = ""
	specific = ""
	flag_type = ""
	command = [
		"youtube-dl ",
		"-o \"%(uploader)s ",
		"%(upload_date)s %(title)s ",
		".%(ext)s\" --sleep-interval 2 "
	]
	exe, format, out_beg, source, o_name, o_end = 0, 0, 1, 1, 2, 3
	vid_try = 1
	for whole_line in playlists :
		th_line = whole_line.split( '\t' )[0] # the rest is a comment
		v_type = th_line[0]
		for_bash = command[exe] + flags[v_type][format] + command[out_beg] \
			+ flags[v_type][source] + command[o_name] \
			+ str(vid_try) + command[o_end]
		if ( v_type == "&" ) :
			for_bash += "--playlist-items "
		for_bash += th_line[2:] # ditch flag and space
		#for_bash = "echo " + for_bash # 4TESTS
		print
		os.system( for_bash )
		vid_try += 1

main()




