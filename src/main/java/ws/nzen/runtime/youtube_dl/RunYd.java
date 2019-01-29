/** see ../../../../../LICENSE for release details */
package ws.nzen.runtime.youtube_dl;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

/**  */
public class RunYd
{
	private static final String cl = "ry.";
	private Map<String, String> typeToTemplate;

	/** @param args */
	public static void main( String[] args )
	{
		final String here = cl +"m ";
		/*
		read file
		for line in file
			assemble process string
			execute
			if bad exit code
				add to complaint list
		*/
		if ( args.length < 1 )
		{
			System.err.println( here +"first argument is a filepath with links in it" );
			return;
		}
		List<String> links;
		try
		{
			links = Files.readAllLines( Paths.get( args[ 0 ] ) );
		}
		catch ( IOException ie )
		{
			System.err.println( here +"couldn't get lines of "+ args[ 0 ]
					+" because "+ ie );
			return;
		}
		int sleepSeconds = 5;
		if ( args.length > 1 )
			sleepSeconds = Integer.valueOf( args[ 1 ] );
		RunYd notCurl = new RunYd();
		notCurl.download( links, sleepSeconds );
	}


	public RunYd()
	{
		fillTemplate( "" );
	}


	private void fillTemplate( String mappingFile )
	{
		final String here = cl +"ft ";
		if ( mappingFile == null || mappingFile.isEmpty() )
		{
			typeToTemplate = new HashMap<>();
			typeToTemplate.put( "&", "%(uploader)s yt %(upload_date)s %(title)s i" ); // youtube playlist
			typeToTemplate.put( "y", "%(uploader)s yt %(upload_date)s %(title)s.%(ext)s\" -f 18" ); // youtube vid
			typeToTemplate.put( "b", "bc %(title)s.%(ext)s\"" ); // http://littlev.bandcamp.com/track/illusive-man
			typeToTemplate.put( "d", "%(uploader)s dm %(upload_date)s %(title)s.%(ext)s\" -f standard" ); // dailymotion
			typeToTemplate.put( "v", "%(uploader)s vi %(upload_date)s %(title)s.%(ext)s\" -f http-360p" ); // vimeo
			typeToTemplate.put( "s", "%(uploader)s sc %(upload_date)s %(title)s.%(ext)s\"" ); // soundcloud
			typeToTemplate.put( "n", "%(uploader)s ng %(id)s %(title)s.%(ext)s\"" ); // newgrounds ; mp3, needn"t -f
		}
	}


	public void download( List<String> links, int sleepSeconds )
	{
		final String here = cl +"d ";
		final int linkInd = 0;
		// COPYPASTA from run_dl.py
		final int y_dl = 0, sleep = y_dl +1, b_dl = sleep +1;
		System.out.println( here +"os "+ System.getProperty( "os.name" ) );
		String[] command = { "youtube-dl -o \"",
							String.format( " --sleep-interval %d ", sleepSeconds ),
		         			"python3 /usr/local/sbin/bc_dl --base-dir=m"
		        			+" --template=\"%{genres}/%{artist}/%{album}/%{track} %{title}\" " };
		if ( ! System.getProperty( "os.name" ).equals( "Linux" ) )
		{
			// NOTE executables end in .exe
			// improve template comes from a file, in the future
			command[ y_dl ] = "youtube-dl.exe -o \"";
		}
		for ( String linkLine : links )
		{
			if ( linkLine.isEmpty() )
				continue;
			String flag = linkLine.substring( 0, linkLine.indexOf( " " ) );
			String rest = linkLine.substring( flag.length() +1 ); // NOTE skip the space
			String[] linkAndComment = rest.split( "\t" );
			if ( typeToTemplate.containsKey( flag )
					&& ! linkAndComment[ linkInd ].isEmpty() )
			{
				// System.out.println( here +"link is "+ linkAndComment[ linkInd ] );
				if ( flag.equals( "&" ) || flag.equals( "b" ) )
				{
					System.out.println( here +"list and bandcamp unimplemented" );
					continue;
				}
				else
				{
					String instruction = command[ y_dl ] + typeToTemplate.get( flag )
							+ command[ sleep ] + linkAndComment[ linkInd ];
					// System.out.println( here +"instruction | "+ instruction );
					List<String> commandComponents = new LinkedList<String>();
					// FIX just hardcoding a valid version for the first use case
					if ( flag.equals( "y" ) )
					{
						commandComponents.add( "youtube-dl" );
						if ( ! System.getProperty( "os.name" ).equals( "Linux" ) )
						{
							commandComponents.set( 0, commandComponents.get( 0 ) +".exe" );
						}
						commandComponents.add( "-o" );
						commandComponents.add( "%(uploader)s yt %(upload_date)s %(id)s %(title)s.%(ext)s" );
						commandComponents.add( "--sleep-interval" );
						commandComponents.add( Integer.toString( sleepSeconds ) );
						commandComponents.add( "-f" );
						commandComponents.add( "18" );
						commandComponents.add( linkAndComment[ linkInd ] );
					}
					else
					{
						// NOTE launcher separates these, so it does not work
						commandComponents.add( instruction );
					}
					ProcessBuilder yourJar = new ProcessBuilder( commandComponents );
					yourJar.inheritIO();
					try
					{
						int resultCode = yourJar.start().waitFor();
						if ( resultCode != 0 )
						{
							System.err.println( here +"saving problem link: "
									+ flag +" "+ linkAndComment[ linkInd ] );
						}
					}
					catch ( IOException ie )
					{
						System.err.println( here +"Couldn't launch downloader because "+ ie );
					}
					catch ( InterruptedException ie )
					{
						System.err.println( here +"Programmatically told to quit via "+ ie );
						return;
					}
				}
			}
		}
	}

}





































