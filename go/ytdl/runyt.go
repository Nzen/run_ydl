
package ytdl

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"strings"
)

func Prep( jsonFilePath string ) Ytdl {
	var original YtArgList
	err := json.Unmarshal( []byte( entireFile( jsonFilePath ) ), &original )
	if err != nil {
		panic( fmt.Sprint(  "invalid json config %v", err ) )
	}
	return Ytdl { original.Flags }
}

func ( hasFormat *Ytdl ) DownloadFrom( args []string ) {
	// NOTE prepping cache
	arg_ind := make( map[ string ]int )
	for ind, oneArg := range hasFormat.Styles {
		arg_ind[ oneArg.Flag ] = ind
	}
	// NOTE prepping common args
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
		if len( line ) == 0 {
			continue
		}
		tabInd := strings.Index( line, "\t" )
		var urlAndFlag string
		if tabInd >= 0 {
			urlAndFlag = line[ : tabInd ]
		} else {
			urlAndFlag = line
		}
		spaceInd := strings.Index( line, " " )
		flag := urlAndFlag[ : spaceInd ]
		url := urlAndFlag[ spaceInd : ]
		formatInd, okness := arg_ind[ flag ]
		if ! okness {
			fmt.Println( "unhandled flag", flag )
		}
		theseArgs := hasFormat.Styles[ formatInd ].StaticArgs
		allArgs := make( []string, len( theseArgs ) +1 )
		for ind, one := range theseArgs {
			allArgs[ ind ] = one
		}
		lastInd := len( allArgs ) -1
		// allArgs[ lastInd -1 ] = "-s"
		allArgs[ lastInd ] = url
		process := exec.Command( ytdlName, allArgs... )
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

// @Deprecated
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

func entireFile( filePath string ) string {
	byteAr, err := ioutil.ReadFile( filePath )
	if ( err != nil ) {
		panic( fmt.Sprint(  "couldn't read file because %v", err ) )
	}
	return string( byteAr )
}

func linesInFile( filePath string ) []string {
	return strings.Split( entireFile( filePath ), "\n" )
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
	knower := ytdl.Prep( "yt_config.json" )
	knower.DownloadFrom( os.Args )
}
	*/






















