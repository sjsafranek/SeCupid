#!/usr/bin/perl 
#===============================================================================
#
#         FILE:  stefan.pl
#
#        USAGE:  ./stefan.pl
#
#  DESCRIPTION:
#
#      OPTIONS:  ---
# REQUIREMENTS:  ---
#         BUGS:  ---
#        NOTES:  ---
#       AUTHOR:  Stefan Safranek, stefan@moonshadowmobile.com
#      COMPANY:
#      VERSION:  1.0
#      CREATED:  03/01/2016 05:01:20 AM
#     REVISION:  ---
#===============================================================================

use DBI;
use DBD::Pg;
# use LWP::UserAgent;
# use JSON::XS;

use strict;
use warnings;

my $filename = shift @ARGV;
print "$filename\n";
open(my $fh, '<:encoding(UTF-8)', $filename)
	or die "Could not open file '$filename' $!";


my $samplefile = 'report.csv';
open(my $fhSample, '>>', $samplefile) or die "Could not open file '$filename' $!";


my $c = 0;
while (my $row = <$fh>) {
	chomp $row;

	print $fhSample "$row\n";

	$c<1 or die;
	$c++;
}


close $fhSample;

close $fh;


# # Database
# my $dbname       = 'stefan';
# my $username     = 'stefan';
# my $password     = 'geolRocks';
# my $port         = 5432;
# my $host         = 'localhost';

# # connect to database
# my $dbh = DBI->connect( "dbi:Pg:dbname=$dbname;host=$host;port=$port;",
# 	$username, $password,
# 	{ AutoCommit => 0, RaiseError => 1, PrintError => 0 } 
# ); 

# # loop through servers
# my $sth = $dbh->prepare("INSERT INTO qs_monitoring (qs_ip, qs_fqdn, qs_full, draining, empty, failed, startups, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
# my @bind_vals = ();
# push(@bind_vals, $server->{ip});
# push(@bind_vals, $server->{fqdn});
# push(@bind_vals, $server->{full});
# push(@bind_vals, $server->{draining});
# push(@bind_vals, $server->{empty});
# push(@bind_vals, $server->{failed});
# push(@bind_vals, $server->{startups});
# push(@bind_vals, $server->{status});
# print "@bind_vals\n";
# $sth->execute(@bind_vals);
# $dbh->commit();

# # disconnect from database
# $dbh->disconnect();

