opendir(IMD, "/Users/isa/Desktop/Providence/William") or die "$!";
@thefiles= readdir(IMD);
close DIR;

$,="\t";

foreach $f (@thefiles)
{
	print STDERR $f."\n";
	open FILE, $f or die $!;

	
while(<FILE>){	
	chomp;
	$_ =~ tr/\015//d;
	if (($_ !~ /CHI/)&&($_ !~ /\%/)&&($_ !~ /@/))
	{
		@parts = split(/\d/);
		@speech= split(/:\t/,$parts[0]);
		$str=$_;
		my @all_nums    = $str =~ /(\d+)/g; #$str =~ s/[^0-9]//g;
		print $all_nums[0],$all_nums[1],$speech[1]."\n";
		
	}
	
}

print "@",$f."\n";
}