from sys import argv
from subprocess import call


try :
	link = argv[ 1 ]
except IndexError:
	link = raw_input( " - which url interests you? " )

try:
	ydl_answ = call( "youtube-dl -F "+ link, shell = True )
	if ydl_answ is not 0 :
		print "-- failed "+ link + " code "+ str(ydl_answ)
except OSError as ose :
	print "Execution failed:", ose
