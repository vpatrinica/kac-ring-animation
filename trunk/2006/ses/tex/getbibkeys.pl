#!/usr/bin/perl

while(<>){
    if(/\s*\@.*\{([\w\.\-]*),/){
	print "\\nocite{$1}\n";
    }
}
