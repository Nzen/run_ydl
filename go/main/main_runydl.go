
package main

import (
	"os"
	"nzen.ws/runtime/ytdl"
)

func main() {
	knower := ytdl.Prep( "yt_config.json" )
	knower.DownloadFrom( os.Args )
}






















