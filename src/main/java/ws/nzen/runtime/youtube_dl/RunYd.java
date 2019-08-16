/** see ../../../../../LICENSE for release details */
package ws.nzen.runtime.youtube_dl;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Option;
import picocli.CommandLine.Parameters;

/**  */
@Command(
		description = "Batch processor of links for youtube-dl",
		name = "RunYdl",
		version = "RunYdl 1.0",
		mixinStandardHelpOptions = true )
public class RunYd implements Runnable
{
	private static final String cl = "ry.";
	private Map<String, String> typeToTemplate;

	@Parameters(
			arity = "1",
			paramLabel = "batch",
			description = "File with links"
			)
	private Path batch;

	@Option(
			names = { "-s", "--sleep" },
			paramLabel = "sleep",
			description = "seconds to wait" )
	private int sleepSeconds = 5;

	/** @param args */
	public static void main( String[] args )
	{
		int exitCode = new CommandLine( new RunYd() ).execute( args );
		System.exit( exitCode );
	}


	public RunYd()
	{
		fillTemplate();
	}


	private void fillTemplate()
	{
		if ( batch == null )
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
		// else parse file for type to template
	}


	public void run()
	{
		final String here = cl +"r ";
		List<String> links;
		try
		{
			links = Files.readAllLines( batch );
		}
		catch ( IOException ie )
		{
			System.err.println( here +"couldn't get lines of "+ batch
					+" because "+ ie );
			return;
		}
		download( links, sleepSeconds );
	}


	public void download( List<String> links, int sleepSeconds )
	{
		/*
		read file
		for line in file
			assemble process string
			execute
			if bad exit code
				add to complaint list
		*/
		final String here = cl +"d ";
		final int linkInd = 0;
		// COPYPASTA from run_dl.py
		final int y_dl = 0, sleep = y_dl +1, b_dl = sleep +1;
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





































