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

def test_playlist_special() :
	here = 't_p_s '
	callee = '& 6 PLCWfs'
	became = laylist_special( callee )
	expected = '6 PLCWs.%(ext)s\" -f 18'
	assert became == expected, here +'didnt cut single digit correctly for playlist'
	callee = '& 46 PLCWfs'
	became = laylist_special( callee )
	expected = '46 PLCWs.%(ext)s\" -f 18'
	assert became == expected, here +'didnt cut two digit correctly for playlist'
	callee = '& 756 PLCWfs'
	became = laylist_special( callee )
	expected = '756 PLCWs.%(ext)s\" -f 18'
	assert became == expected, here +'didnt cut triple digit correctly for playlist'

def build_command( title_vars, th_line ) :
	y_dl, sleep = 0, 1
	for_bash = ""
	flag_type = ""
	#
	command = [ "youtube-dl -o \"", " --sleep-interval 5 " ]
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
		# except KeyError: '' + command[sleep]
	for_bash += th_line[2:] # ditch flag and space, rest is the link
	# for_bash = "echo " + for_bash # 4TESTS / make a cli arg instead of toggling this?
	return for_bash

def test_build_command( title_vars ) :
	here = 't_b_c '
	""" 	for when I'm ready
	became = build_command( title_vars, callee )
	expected = ''
	assert became == expected, here +'didnt cut triple digit correctly for playlist'
	"""
	callee = '& 6 PLCWfJLGX7Ygo'
	print( build_command( title_vars, callee ) )
	callee = 'y Dv966FgifL8'
	print( build_command( title_vars, callee ) )
	callee = 's https://soundcloud.com/grillmarketing/fun-we-are-young'
	print( build_command( title_vars, callee ) )
	callee = 'r https://www.reverbnation.com/TheDealersUs/song/22237152-in-my-sleep'
	print( build_command( title_vars, callee ) )
	callee = 'b http://daysndaze.bandcamp.com/track/rockabilly-impending-deathfuture'
	print( build_command( title_vars, callee ) )
	callee = 'c https://www.mixcloud.com/Auzy5/liquid-techno-logy-3/'
	print( build_command( title_vars, callee ) )
	callee = 'v https://vimeo.com/71278954'
	print( build_command( title_vars, callee ) )
	callee = 'n http://www.newgrounds.com/audio/listen/65711'
	# would I want http://www.newgrounds.com/portal/view/77750 ?
	print( build_command( title_vars, callee ) )
	callee = 'b http://littlev.bandcamp.com/track/illusive-man'
	print( build_command( title_vars, callee ) )
	callee = 'd http://www.dailymotion.com/video/x2w4572_bioshock-infinite-trailer_videogames'
	print( build_command( title_vars, callee ) )
	callee = 'h xhamster.com/movies/2318103/lexxxi_luxe.html'
	print( build_command( title_vars, callee ) )

def list_failed( failed ) :
	if len( failed ) > 0 :
		file = open( str(len( failed ))+ " couldnt dl.txt", 'w' )
		for vid in failed :
			file.write( vid +"\r\n " )
		file.close()
		print( " --- check for failed urls" )

def save_failed( what_happened, failed ) :
	failed.append( what_happened )
	print( "-- saving failed for later --" )

def main( playlist, title_vars ) :
	failed = []
	for whole_line in playlist :
		if whole_line[0] in title_vars :
			for_bash = build_command( title_vars, whole_line.split( '\t' )[0] )
			print()
			try:
				ydl_answ = call( for_bash, shell = True )
				if ydl_answ is not 0 :
					save_failed( str(ydl_answ) +" :: "+ whole_line, failed )
			except OSError as ose :
				print( "Execution failed:", ose )
		else :
			save_failed( "unknown web flag "+ whole_line[0], failed )
	list_failed( failed )

def test_main() :
	# am I splitting like I expect ?
	here = 't_m '
	callee = 'y https://www.youtube.com/watch?v=chFBWY7a9GI	ec social game'
	became = callee.split( '\t' )[0]
	expected = [ 'y https://www.youtube.com/watch?v=chFBWY7a9GI' ]
	assert became == expected, here +'splitting wrong'

def test( title_vars ) :
	test_main()

title_vars = {
'&' : '%(uploader)s yt %(upload_date)s %(title)s i', # youtube playlist
'y' : '%(uploader)s yt %(upload_date)s %(title)s.%(ext)s\" -f 18', # youtube vid
'b' : 'bc %(title)s.%(ext)s\"', # http://littlev.bandcamp.com/track/illusive-man
'd' : '%(uploader)s dm %(upload_date)s %(title)s.%(ext)s\" -f standard', # dailymotion
'v' : '%(uploader)s vi %(upload_date)s %(title)s.%(ext)s\" -f h264-sd', # vimeo
's' : '%(uploader)s sc %(upload_date)s %(title)s.%(ext)s\"', # soundcloud
'n' : '%(uploader)s ng %(id)s %(title)s.%(ext)s\"', # newgrounds ; mp3, needn't -f
'r' : '%(uploader)s rn %(id)s %(title)s.%(ext)s\"', # reverbnation
'm' : '%(uploader)s vm %(upload_date)s %(title)s.%(ext)s\"', # vidme
'h' : '%(uploader)s xh %(upload_date)s %(title)s.%(ext)s\" -f sd',# xhamster
} # out here, as I suspect it's a bit heavy to recreate everytime

try :
	fileN = argv[ 1 ]
except IndexError:
	fileN = raw_input( " - which file has the urls? " )
if fileN == 'test' :
	test( title_vars )
else :
	file = open( fileN )
	playlist = file.readlines()
	file.close()
	main( playlist, title_vars )




