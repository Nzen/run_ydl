'''
 - file format -
[flag] [csv playlist nums]* [url]
'''
from sys import argv

def main( queue, old_file_name ) :
	file_out = open( 'new_'+ old_file_name, 'w' )
	for whole_line in queue :
		ind_of_tab = whole_line.find( '\t' )
		if ind_of_tab < 0 :
			ind_of_tab = len( whole_line )
		ind_of_and = whole_line.find( '&', 1, ind_of_tab )
		if ind_of_and >= 0 :
			file_out.write( whole_line[ 0 : ind_of_and ] \
				+ whole_line[ ind_of_tab : len( whole_line ) ] +'\n' )
		else :
			file_out.write( whole_line[ 0 : len( whole_line ) ] )
	file_out.close()

try :
	orig_file_name = argv[ 1 ]
except IndexError:
	orig_file_name = raw_input( " - which file has the urls? " )
if orig_file_name == 'test' :
	test( title_vars )
else :
	file_out = open( orig_file_name )
	queue = file_out.readlines()
	file_out.close()
	main( queue, orig_file_name )
