'''
 - file format -
[flag] [csv playlist nums]* [url]
'''
from sys import argv
from subprocess import call

def playlist_special( th_line ) :
	# unrolled: yt doesn't have len( playlist ) > 999
	en = 4 # two digit
	if th_line[en -1] is " " : # single digit
		en -= 1
	elif th_line[en +1] is " " : # three digit
		en += 1
	return th_line[2:en] +".%(ext)s\" -f 18"

def build_command( title_vars, th_line ) :
	y_dl, sleep = 0, 1
	for_bash = ""
	flag_type = ""
	#
	command = [ "youtube-dl -o \"", " --sleep-interval 2 " ]
	v_type = th_line[0]
	for_bash = command[y_dl]
	if v_type is "&" : # if you do more than one, add -i here
		for_bash += title_vars[v_type] + playlist_special( th_line ) \
		+ command[sleep] + "--playlist-items "
	elif v_type is "b" :
		name_start = 9
		period = th_line.find(".", name_start)
		for_bash += th_line[name_start : period] +" " \
		+ title_vars[v_type]+ command[sleep]
	else :
		for_bash += title_vars[v_type] + command[sleep]
	for_bash += th_line[2:] # ditch flag and space, rest is the link
	# for_bash = "echo " + for_bash # 4TESTS / make a cli arg instead of toggling this?
	return for_bash

def list_failed( failed ) :
	if len( failed ) > 0 :
		file = open( str(len( failed ))+ " couldnt dl.txt", 'w' )
		for vid in failed :
			file.write( vid +"\r\n " )
		file.close()
		print " --- check for failed urls"

def main( playlist ) :
	title_vars = {
	'&': '%(uploader)s yt %(upload_date)s %(title)s i',
	'y' : '%(uploader)s yt %(upload_date)s %(title)s.%(ext)s\" -f 18',
	'b' : 'bc %(title)s.%(ext)s\"', # http://littlev.bandcamp.com/track/illusive-man
	'd' : '%(uploader)s dm %(upload_date)s %(title)s.%(ext)s\" -f standard',
	'v' : '%(uploader)s vi %(upload_date)s %(title)s.%(ext)s\" -f h264-sd',
	's' : '%(uploader)s sc %(upload_date)s %(title)s.%(ext)s\"',
	'n' : '%(uploader)s ng %(id)s %(title)s.%(ext)s\"' # mp3, needn't -f
	} # out here, as I suspect it's a bit heavy to recreate everytime
	failed = []
	for whole_line in playlist :
		for_bash = build_command( title_vars, whole_line.split( '\t' )[0] )
		print
		try:
			ydl_answ = call( for_bash, shell = True )
			if ydl_answ is not 0 :
				failed.append( ydl_answ +" :: "+ whole_line )
				print "-- saving failed for later --"
		except OSError as ose :
			print "Execution failed:", ose
	list_failed( failed )

try :
	fileN = argv[ 1 ]
except IndexError:
	to_pause = raw_input( " - which file has the urls? " )
#
file = open( fileN )
playlist = file.readlines()
file.close()
#
main( playlist )




