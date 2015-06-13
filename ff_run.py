'''
	FF_RUN
Author:  Nicholas (Nzen)
License: [WTFPL](www.wtfpl.net)

Assumptions:
 python 2.7
 ffmpeg installed and on the Path
 no files/folders with a name less than six characters

Usage:
 put this module with the files to convert
 create "done" folder
 run this module
 converted mp3s appear in the done folder
 if Attentive flag (to limit cpu heat)
	need to press a key per 15 conversions, bell signals need
 sounds double bell when finished
'''

import os

class Fsm( object ) :
	'''
	Later: remove quotes, underscore to spaces. But not PDA stuff, please :p
	'''

	def __init__( self, phrase ) :
		self.full = phrase
		self.lim = len( phrase )
		self.curr = 0
		self.next = 0
		self.orig = 0
		self.trans = self.rvfX # fn pointer for state transitions
		self.temp = ""
		#self.build = ""
		#self.d_last = -1
		self.notDone = True
		self.lexToken = {
			self.rvfX : "x",
			self.rvfSpI : "\'",
			self.rvfSpR : "\"",
			self.rvfHyI : "-",
			self.rvfHyR : "=",
			self.rvfDtI : ".",
			self.rvfDtR : "f"
		}

	def rvfX( self ) : # I could almost just make an adjacency table
		if self.temp == ' ' :
			self.trans = self.rvfSpI
		elif self.temp == '.' :
			self.trans = self.rvfDtI
		else :
			self.trans = self.rvfX

	def rvfSpI( self ) :
		if self.temp == '-' :
			self.trans = self.rvfHyI
		elif self.temp == ' ' :
			self.trans = self.rvfSpI # consider splitting to shorten 'f  f'
		elif self.temp == '.' :
			self.trans = self.rvfDtI
		else :
			self.trans = self.rvfX

	def rvfHyI( self ) :
		if self.temp == '-' :
			self.trans = self.rvfHyI
		elif self.temp == ' ' :
			self.trans = self.rvfSpR
		elif self.temp == '.' :
			self.trans = self.rvfDtI
		else :
			self.trans = self.rvfX

	def rvfSpR( self ) :
		if self.temp == '-' :
			self.trans = self.rvfHyR
		elif self.temp == ' ' :
			self.trans = self.rvfSpR
		elif self.temp == '.' :
			self.trans = rvfDtI
		else :
			self.trans = self.rvfX
			# self.replace( " " ) # reactivate when transitions work

	def rvfHyR( self ) :
		if self.temp == '-' :
			self.trans = self.rvfHyR
		elif self.temp == ' ' :
			self.trans = self.rvfSpR
		elif self.temp == '.' :
			self.trans = self.rvfDtI
		else :
			self.trans = self.rvfX
			# self.replace( " " ) # reactivate when transitions work
			# this & below are why I am not making an adjacency table
			# of course, I could handle these cases separately

	def rvfDtI( self ) :
		if self.temp == '.' :
			self.trans = self.rvfDtR
			# d_last = curr
		else :
			self.trans = self.rvfX

	def rvfDtR( self ) :
		if self.temp == '.' :
			self.trans = self.rvfDtR
			# d_last += 1
		else :
			self.trans = self.rvfX

	def printNext( self ) :
		print self.lexToken[ self.trans ],

	def replace( self, withWhat ) :
		'''
		cut from orig to curr
		replace from orig to curr, withWhat
		orig = curr
		'''
		return

	def check( self ) :
		self.notDone = ( self.curr < self.lim )

	def eval( self ) :
		while self.notDone :
			self.temp = self.full[ self.curr ]
			moveTo = self.trans
			moveTo()
			self.printNext()
			self.curr += 1
			self.check()

def removeViaFsm( name ) :
	'yay optimize'
	print
	for lett in name :
		print lett,
	print
	state = Fsm( name )
	state.eval()
	# print " ended at " + str( state.curr ) + ", last was " + state.temp
	return state.temp # + "mp3"

def fsmVersion() :
	'test fsm before promoting to real'
	cases = {
		"banana" : "banana",
		"in.io" : "in.",
		"barn - barn.f" : "barn barn.",
		"a  b   - --  b.f" : "a b b.",
		"a..dc.ac" : "a.dc."
	}
	result = ""
	print "\nlegend: x(\\w) \'(\\s1) \"(\\s2) -(-1) =(-2) .(.1) f(.2)"
	#probs = [] # later for test robustness
	for test in cases :
		result = removeViaFsm( test )
		if result != cases[test] :
			print "\n>" + result + "< didn't match"
			# currently printing lex tokens above, so no need to print again
			# currently not editing
		# don't forget, won't print in order :B

#	-	-	-	-

def hyphenAlone( name, inde ) :
	'is there a substring " - "? '
	return sp( name[inde] ) and hy( name[inde+1] ) and sp( name[inde+2] )

def countHyAlone( name ) :
	'how many isolated hyphens in this name?'
	times = 0
	for inde in range( 1, len(name)-4 ) :
		if hyphenAlone( name, inde ) :
			times += 1
	return times

def findsMultiHyphen() :
	'shows which files have more than one isolated hyphen'
	here = os.getcwd()
	for_bash = ""
	temp = ""
	for thisFile in os.listdir( here ) :
		# necessary, protected files
		if thisFile == "ff_run.py" or thisFile == "done":
			# if os.path.isdir( here + \ + thisFile )
			continue
		if countHyAlone( thisFile ) > 1 :
			print thisFile + '\n'
	print '\7\7' # double bell when done

#	-	-	-	-

def sp( aChar ) :
	'is space?'
	return aChar == " "

def hy( aChar ) :
	'is hyphen?'
	return aChar == "-"

def removeHyphen( name ) :
	' if " - " return " ". '
	for inde in range( 1, len(name)-4 ) :
		if hyphenAlone( name, inde ) :
			return name[ :inde ] + name[ inde+2: ]
	return name

def n_index( fileExt ) :
	'index of final period (for extension), plus .. -> .'
	for ind in range( -2,-6,-1 ) :
		if fileExt[ ind ] == "." :
			if fileExt[ ind - 1 ] == "." :
				return ind - 1
			else :
				return ind
	return 1

def new_name( fileExt ) :
	'name ending in mp3 without some extras'
	#bla - g..webm -> bla g.mp3 || bla.markdown -> 1
	fileExt = removeHyphen( fileExt )
	lit_ind = n_index( fileExt )
	if lit_ind > 0 :
		return lit_ind
	return fileExt[ :lit_ind+1 ] + "mp3"

def simpleVersion( attentive ) :
	'for each file except this one, convert to mp3 with ffmpeg'
	# CLI > ffmpeg -i "in put.bna" -vn "out put.apl"
	command = "ffmpeg -i \""
	out_flag = "\" -vn \"done\\" # done is a preexisting out-folder
	here = os.getcwd()
	problems = []
	processed = 0
	for_bash = ""
	temp = ""
	#lim = 0
	for thisFile in os.listdir( here ) :
		# necessary, protected files
		if thisFile == "ff_run.py" or thisFile == "done":
			# if os.path.isdir( here + \ + thisFile )
			continue
		temp = new_name( thisFile )
		if temp == 1 :
			problems.append( thisFile )
			continue
		for_bash = command + thisFile + out_flag + temp + "\""
		'''	for quick testing
		lim += 1
		if lim > 20 :
			break
		print for_bash
		'''
		processed += 1
		if attentive and processed > 15 :
			raw_input( "\7\n pausing to give cpu a breather, press ENTER" )
			processed = 0
		os.system( for_bash )
	if len( problems ) > 0 :
		print "\n PROBLEMS: "
		for nameSigh in range( 0, len( problems ) ) :
			print problems[ nameSigh ]
	print '\7\7' # double bell when done

def main() :
	'choose what this does'
	checkInEvery30Seconds = True # am I willing to baby sit the conversion?
	simpleVersion( checkInEvery30Seconds )
	# fsmVersion()
	# findsMultiHyphen()

main()











