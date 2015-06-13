'''
 - file format -
[flag] [csv playlist nums]* [url]
'''
import os
from sys import argv
from subprocess import call

def playlist_special( th_line ) :
	en = 4
	if th_line[en -1] is " " :
		en -= 1
	return th_line[2:en] +".%(ext)s\" -f 18"

def main( fileN ) :
	for_bash = ""
	flag_type = ""
	command = [ "youtube-dl -o \"", " --sleep-interval 2 " ]
	output = {
	'&': '%(uploader)s yt %(upload_date)s %(title)s i',
	'y' : '%(uploader)s yt %(upload_date)s %(title)s.%(ext)s\" -f 18',
	'b' : 'bc %(title)s.%(ext)s\"', # http://littlev.bandcamp.com/track/illusive-man
	'd' : '%(uploader)s dm %(upload_date)s %(title)s.%(ext)s\" -f standard',
	'v' : '%(uploader)s vi %(upload_date)s %(title)s.%(ext)s\" -f h264-sd',
	's' : '%(uploader)s sc %(upload_date)s %(title)s.%(ext)s\"',
	'n' : '%(uploader)s ng %(id)s %(title)s.%(ext)s\"' # mp3, needn't -f
	}
	y_dl, sleep = 0, 1
	failed = []
	file = open( fileN )
	playlist = file.readlines()
	file.close()
	for whole_line in playlist :
		th_line = whole_line.split( '\t' )[0] # the rest is a comment
		v_type = th_line[0]
		for_bash = command[y_dl]
		if v_type is "&" : # if you do more than one, add -i here
			for_bash += output[v_type] + playlist_special( th_line ) \
			+ command[sleep] + "--playlist-items "
		elif v_type is "b" :
			name_start = 9
			period = th_line.find(".", name_start)
			for_bash += th_line[name_start : period] +" " \
			+ output[v_type]+ command[sleep]
		else :
			for_bash += output[v_type] + command[sleep]
		for_bash += th_line[2:] # ditch flag and space, rest is the link
		for_bash = "echo " + for_bash # 4TESTS
		print
		try:
			ydl_answ = call( for_bash, shell = True )
			if ydl_answ is not 0 :
				failed.add( th_line[2:] )
		except OSError as ose :
			print "Execution failed:", ose
	if len( failed ) > 0 :
		file = open( "didnt "+ fileN, 'w' )
		for vid in failed :
			file.write( vid +"\r\n" )
		file.close()
		print " --- check for failed urls"

try :
	fileN = argv[ 1 ]
except IndexError:
	print " - which file has the urls?"
	exit( 0 )
main( fileN )




