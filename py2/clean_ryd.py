
'''
The current naming scheme for run_yd assumes I don't know which failed and can't even retry them until the user reruns run_yd. So, I need a little script to cut those number tags after I'm done. However, this will really be a test for the next version of run_yd that harvests outputs and doesn't even need cleanup.
'''
import os
import string
import subprocess

def not_from_run_yd( front ) :
	return front[0] is not 'n' and front[1] not in string.digits

def has_pl_i( front ) :
	return front[0] is 'i' and front[1] in string.digits

def cleanup( filename ) :
	'to ryl files- cuts run number, moves potential play num to back'
	# n9 i1  BmSt32 [ bla bla ]nguin.mp4   | typical in
	# BmSt32 [ bla bla ]nguin i1.mp4   | intended out
	misnamed = True
	if not_from_run_yd( filename[ :3] ) :
		#print " ---- skipped "+ filename # 4TESTS
		return not misnamed, ""
	f_letter = 2
	p_num = "" # playlist number
	f_letter = filename.find(" ") +1
	if has_pl_i( filename[ f_letter:f_letter +2 ] ) :
		pl_end = 3
		if filename[ f_letter +2 ] is ' ' :
			pl_end = 2 # index is single digit, but next is an extra space
		p_num = " "+ filename[ f_letter : f_letter +pl_end ] # won't vary
		f_letter += 4
		#print p_num +"|| "+ filename[ :9 ]# 4TESTS
	ext = filename[ -4:] # .mp4
	return misnamed, filename[ f_letter : -4 ]+ p_num + ext

def rename( old, new )	:
	'os renames old to new' # this is the future direction part
	#old.write( new +'\r\n' ) # 4TESTS
	try:
		command = "ren " # on windows; "mv " on linux
		command += "\""+ old +"\" \""+ new +"\""
		retcode = subprocess.call( command, shell = True )
		#retcode = subprocess.call( "youtube-dl x2GpemFeMtI",shell=True ) known fail
		if retcode is not 0 :
			print "Returned- ", retcode # 0 success, 1 fail, -1 terminated
	except OSError as ose :
		print "Execution failed:", ose # starts with a space

def main() :
	'get names, clean them, rename'
	needed = True
	here = os.getcwd()
	#output = open( "renames.txt", 'w' ) # 4TESTS
	for directory_tuple in os.walk( here ) :
		# yields a 3-tuple (dirpath, dirnames, filenames)
		for current_f in directory_tuple[2] :
			needed, future_f = cleanup( current_f )
			if needed :
				rename( current_f, future_f ) # output, future_f)
	#output.close() # 4TESTS
	#rename( "renames.txt", "touched.txt" ) # 4TESTS

main()











