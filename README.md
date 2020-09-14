# network_protocol_analysis
Python script to do DNS, nameserver, http protocol analysis etc. of 2 websites of choice.

usage: 
  protocol_analysis --website1 <website_1> --website2 <website_2> --OPTION
where OPTION in [--measure, --help, --asnlinks, --dns, --traces]
e.g: protocol_analysis --website1 wikipedia.org --website2 wits.ac.za --dns

Prerequisites:
  -Must have ASN and City Geolite Databases in geolite_dbs/GeoLite2-ASN_20200721/GeoLite2-ASN.mmdb and
    geolite_dbs/GeoLite2-City_20200721/GeoLite2-City.mmdb to run --asnlinks and --dns.
  -With --measure, new results are written to website_1_trace.txt etc. overwriting any previous file with previous traces
  -Project already comes with already measured traceroute results from Ripe in the files website_1_trace.txt
   and website_2_trace.txt so running --asnlinks or --traces will work.
