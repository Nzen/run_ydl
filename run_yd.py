import os
from sys import argv

'''
youtube-dl is great, but it doesn't seem to grab playlist arguments from a batch file.
As I don't want a whole playlist at once, this module solves that limitation.

moving forward, I may just have flags for every video (macro supplied)
 that way, I can intersperse soundcloud etc. Not tonight

 - file format -
\d+(,\d+)* [\d-_\w]+

 - cli run -
python run_yd.py [username@google_expects] \"[password_may_need_escaping]\"

 - out to system -
youtube-dl -f 18 -o "%(uploader)s %(upload_date)s %(title)s.%(ext)s" --playlist-items 6,7,8 [playlist_url]
'''

def main( username ) :
	file = open( "0.txt" ) # or your preference, argv also possible
	playlists = file.readlines()
	file.close()

	for_bash = ""
	specific = " -i "
	command = "youtube-dl -f 18 -o \"%(uploader)s %(upload_date)s %(title)s.%(ext)s\" "
	identity = "-u "+ username +" -p \"bla\" "
	for th_line in playlists :
		if ( th_line[0] == "&" ) :
			specific = "-i --playlist-items " + th_line[ 2: ] # NOTE full flag includes a space
		else :
			specific = " -i "+ th_line
		#for_bash = "echo " + command + identity + specific # 4TESTS
		for_bash = command + identity + specific
		os.system( for_bash )

script, username = argv
main( username )
