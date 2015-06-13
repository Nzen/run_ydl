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
import os
from sys import argv

def main( fileN ) :
	for_bash = ""
	flag_type = ""
	command = [ "youtube-dl -o \"n", " --sleep-interval 2 " ]
	output = {
	'&': ' %(uploader)s yt %(upload_date)s %(title)s.%(ext)s\" -f 18',
	'y' : ' %(uploader)s yt %(upload_date)s %(title)s.%(ext)s\" -f 18',
	'b' : ' bc %(title)s.%(ext)s\"',
	'd' : ' %(uploader)s dm %(upload_date)s %(title)s.%(ext)s\" -f standard',
	'v' : ' %(uploader)s vi %(upload_date)s %(title)s.%(ext)s\" -f h264-sd',
	's' : ' %(uploader)s sc %(upload_date)s %(title)s.%(ext)s\"',
	'n' : ' %(uploader)s ng %(id)s %(title)s.%(ext)s\"'
	}
	o_beg, o_end = 0, 1
	vid_try = 1
	file = open( fileN )
	playlist = file.readlines()
	file.close()
	for whole_line in playlist :
		th_line = whole_line.split( '\t' )[0] # the rest is a comment
		v_type = th_line[0]
		for_bash = command[o_beg] + str(vid_try)
		if ( v_type == "&" ) : # if you do more than one, add -i here
			for_bash += " i" + th_line[2:4] + output[v_type] \
			# grabbing 2 chars, often a space. trim()
			+ command[o_end] + "--playlist-items "
		else :
			for_bash += output[v_type] + command[o_end]
		for_bash += th_line[2:] # ditch flag and space, rest is the link
		for_bash = "echo " + for_bash # 4TESTS
		print
		os.system( for_bash )
		vid_try += 1

try :
	fileN = argv[ 1 ]
except IndexError:
	print " - which file has the urls?"
	exit( 0 )
main( fileN )




