#!/usr/bin/perl -i

$match = 0;

if($ARGV[0] eq '-w'){
    shift;
    $silent = 1;
}

while(<>){
    unless(/title.*=/i){
	print unless $silent;
    }
    else{
#	print "TITEL IST HIER\n";
	print $`.$& unless $silent;
	$value = $';  #'
	while(($value =~ /\{/g) > ($value =~ /\}/g)){
	    chomp $value;
	    $value .= ' ' . <>;
	}
	if(($value =~ /\{/g)>1 || ($value =~ /\"/)){
	    print $value unless $silent;
	    next;
	}
  
	$control = 0;
	foreach $w (split /\b/, $value){
	    @CAPITALS = ((' '.$w) =~ m/([A-Z])/g);
	    if(@CAPITALS>1 and not $control){
		if($silent){
		    print "$ARGV: $w\n";
		}
		else{
		    print "{$w}";
		}
		++$match;
	    }
	    else{
		print $w unless $silent;
	    }
	    $control = ($w =~ /\\/g);
	}
    }
}

#if($match){
#    print STDERR $ARGV, " $match matches.\n";
#}
