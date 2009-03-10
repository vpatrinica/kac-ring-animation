#!/usr/bin/perl

use File::Find;

open (COMBINED,">combined.bib") || die "Cannot open combined2.bib:$!";

find(\&cat,'.');

close COMBINED;

opendir DOT, '.';
foreach $fn(readdir DOT){
    if($fn =~ /^(.*bu.*)\.aux$/){
	system("bibtex $1");
    }
}
closedir DOT;

sub cat{
    my $fn = $_;

    local($_);

    print "Checking $fn\n";


    return unless $fn =~ /\.bib$/;
    return if $fn =~ /combined/;

    open (IN, $fn) || die "Cannot open $fn:$!";
    while(<IN>){
	print COMBINED;
    }
    close IN;
}
