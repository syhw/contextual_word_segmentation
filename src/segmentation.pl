opendir(IMD, "/Users/isa/Desktop/Providence/ProvidenceCorpus/bykids") or die "$!";
@thefiles= readdir(IMD);
close DIR;

$,="\t";

foreach $f (@thefiles)
{
	#print STDERR $f."\n";
	if($f =~ /all/)
	{
		open(INFILE, $f);
		@lines = <INFILE>;
		close(INFILE);
		@parts = split("\t", $lines[0]);
		$end=$parts[1];
		print $lines[0];
		$count =0;
		
		for (my $i = 1; $i <= $#lines; $i++)
		{	
			$_=$lines[$i];
			chomp;
			
			if($_ !~ /@/)
			{	
				@parts = split("\t");
				$start=$parts[0];
				if(($start-$end > 60000)&& ($start =~ /^[0-9]+$/))
				{
					$diff= $start-$end;
					#print STDERR $diff."\n";
					print "@\n";
					$count = $count+ 1;
				}
				print $lines[$i];
				if  ($start =~ /^[0-9]+$/)
				{
				$end = $parts[1];}
		 
			}
			else
			{
				$count = $count+ 1;
				print $_."\n";
				@parts = split("\t",$lines[$i+1]);
				$end = $parts[1];
			}
			
		}	
		print STDERR $f,$count."\n";


	}

}