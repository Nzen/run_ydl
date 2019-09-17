
package ytdl

type Ytdl struct {
	Styles []YtArg
}

type YtArg struct {
	Desc string
	Flag string
	StaticArgs []string
}

type YtArgList struct {
	jschema string
	schema_version string
	Flags []YtArg
}





















