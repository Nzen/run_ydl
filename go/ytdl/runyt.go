
package ytdl

import (
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"strings"
)

func Run( args []string ) {
	/*
	get config
	open file
	for line in file
		os call bla
	*/
	var filename string
	if len( args ) > 1 {
		filename = args[ 1 ]
	} else {
		filename = "0.txt"
	}
	var ytdlName string
	if osIsWindows() {
		ytdlName = "youtube-dl.exe"
	} else {
		ytdlName = "youtube-dl"
	}
	lines := linesInFile( filename )
	problems := make( []string, 2 )
	for _, line := range lines {
		tabInd := strings.Index( line, "\t" )
		var urlAndFlag string
		if tabInd >= 0 {
			urlAndFlag = line[ : tabInd ]
		} else {
			urlAndFlag = line
		}
		var url string
		var formatCmd string
		var dlFormat string
		if strings.HasPrefix( urlAndFlag, "y " ) {
			url = urlAndFlag[ 2: ]
			formatCmd = "%(uploader)s yt %(upload_date)s %(title)s.%(ext)s"
			dlFormat = "18"
		} else {
			url = urlAndFlag
			formatCmd = ""
			dlFormat = "10"
		}
		process := exec.Command( ytdlName, "-o", formatCmd, "-f", dlFormat, url )
		process.Stdout = os.Stdout
		err := process.Run()
		if err != nil {
			problems = append( problems, line )
		}
	}
	for _, currProblem := range problems {
		if len( currProblem ) > 0 {
			fmt.Println( "problem with :- ", currProblem )
		}
	}
}

func linesInFile( filePath string ) []string {
	byteAr, err := ioutil.ReadFile( filePath )
	if ( err != nil ) {
		panic( fmt.Sprint(  "couldn't read file because %v", err ) )
	}
	entireText := string( byteAr )
	return strings.Split( entireText, "\n" )
}

// simple heuristic based
func osIsWindows() bool {
	return os.Getegid() == -1
}

	/* NOTE example of running
package main

import (
	"os"
	"nzen.ws/runtime/ytdl"
)

func main() {
	rYtdl()
}

func rYtdl() {
	ytdl.Run( os.Args )
}
	*/






















