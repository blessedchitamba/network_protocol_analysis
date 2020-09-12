#First 
import dns
import dns.resolver
import sys, getopt
import json
import geoip2.database
import time
import subprocess
from pprint import pprint
from datetime import datetime
from ripe.atlas.cousteau import (
  Ping,
  Traceroute,
  AtlasSource,
  AtlasCreateRequest,
  AtlasResultsRequest
)


def send_ripe_measurement_request(website, ATLAS_API_KEY):
	traceroute1 = Traceroute(
		af=4,
		target=website,
		description="testing",
		protocol="ICMP",
	)

	source1 = AtlasSource(
		type="country",
		value="CA", #, canada "CA", "PL", "AU", "AR"],
		requested=3,
		tags={"include":["system-ipv4-works"]}
	)

	source2 = AtlasSource(
		type="country",
		value="ZA", #, South Africa "CA", "PL", "AU", "AR"],
		requested=3,
		tags={"include":["system-ipv4-works"]}
	)

	source3 = AtlasSource(
		type="country",
		value="DE", #, Germany "CA", "PL", "AU", "AR"],
		requested=3,
		tags={"include":["system-ipv4-works"]}
	)

	source4 = AtlasSource(
		type="country",
		value="NG", #, Nigeria "CA", "PL", "AU", "AR"],
		requested=3,
		tags={"include":["system-ipv4-works"]}
	)

	source5 = AtlasSource(
		type="country",
		value="BR", #, Brazil "CA", "PL", "AU", "AR"],
		requested=3,
		tags={"include":["system-ipv4-works"]}
	)

	atlas_request = AtlasCreateRequest(
		start_time=datetime.utcnow(),
		key=ATLAS_API_KEY,
		measurements=[traceroute1],
		sources= [source1, source2, source3, source4, source5],
		is_oneoff=True
	)

	is_success, response = atlas_request.create()
	result_id = []
	if is_success:
		result_id = response['measurements']
		print(result_id)
		return result_id
	else:
		print("Measurement not successful")
		return []

def fetch_ripe_result(result_id, output_file):
	#fetch the result
	kwargs = {
		"msm_id": result_id,
	}

	#while not_fetched:
	is_success, results = AtlasResultsRequest(**kwargs).create()
	if is_success:
		count=1
	#if len(results)!=0:
		#not_fetched = False
		print(len(results))
		for res in results:
			print(count, ":Source address: ",res['src_addr'])
			# result_size = len(res['result'])
			# print("Destination address: ",res['result'][result_size-1]['result'][1]['from'])
			# print("")
			count+=1
		with open(output_file, 'w') as outfile:
			json.dump(results, outfile)

def find_nameservers(website, myResolver):
	print(website, "has the following nameservers:")
	try:
		result = myResolver.resolve(website, 'NS')
		for nameserver in result:
			print('nameserver:', nameserver.to_text())
	except:
		print("There was an error...")

def check_ipv4(website, myResolver):
	print("Checking for ipv4 support in",website,":")
	try:
		result = myResolver.resolve(website, 'A')
		for ipv4 in result:
			print('ipv4:', ipv4.to_text())
	except:
		print("There was an error...")

def check_ipv6(website, myResolver):
	print("Checking for ipv6 support in",website,":")
	try:
		result = myResolver.resolve(website, 'AAAA')
		for ipv6 in result:
			print('ipv6:', ipv6.to_text())
	except:
		print("There was an error...")

def find_cdns(trace_data):
	filename = trace_data
	asn_path = []
	pathToDb = "C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/geolite_dbs/GeoLite2-City_20200721/GeoLite2-City.mmdb"
	pathToAsnDb = "C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/geolite_dbs/GeoLite2-ASN_20200721/GeoLite2-ASN.mmdb"

	with geoip2.database.Reader(pathToDb) as reader:
		with geoip2.database.Reader(pathToAsnDb) as asn_reader:
			with open(filename) as json_file:
				data = json.load(json_file)
				count=1
				#loop through each array item in the json and geolocate the destination address in each trace hop
				for result in data:
					try:
						asn_response = asn_reader.asn(result['src_addr'])
						asn = asn_response.autonomous_system_number
						asn_path.append(str(asn))
					except:
						asn = "Source ASN unknown"
						asn_path.append(asn)
					print("Result number",count,"from address",result['src_addr'],"from ASN",asn)
					count+=1
					for tracert in result['result']:
						#first try get tracert['result'][1]['from'] if it exists
						if tracert['result'][1]!={"x": "*"}:
							hop_ip = tracert['result'][1]['from']
							#geolocate the ip
							try:
								asn_response = asn_reader.asn(hop_ip)
								response = reader.city(hop_ip)
								asn = asn_response.autonomous_system_number
								asn_path.append("->"+str(asn))
								city = response.city.name
								print(hop_ip, city, asn)
							except:
								print("IP not in database")
					print("ASN path taken from address",result['src_addr'],"to destination:")
					print_asn_paths(list(dict.fromkeys(asn_path)))
					asn_path.clear()
					print("")

def print_asn_paths(asn_path):
	for asn in asn_path:
		print(asn, end="")
	print('\n')

def main(argv):
	website_1 = ''
	website_2 = ''
	ATLAS_API_KEY = "9b81eb94-44fe-4e2e-aca7-508b94b7041b"
	if len(sys.argv)==3:
		website_1 = sys.argv[1]
		website_2 = sys.argv[2]
		myResolver = dns.resolver.Resolver()

		#start with the nameservers of each website
		# find_nameservers(website_1, myResolver)
		# find_nameservers(website_2, myResolver)
		# check_ipv4(website_1, myResolver)
		# check_ipv4(website_2, myResolver)
		# check_ipv6(website_1, myResolver)
		# check_ipv6(website_2, myResolver)
		# res_id_1 = send_ripe_measurement_request(website_1, ATLAS_API_KEY)
		# res_id_2 = send_ripe_measurement_request(website_2, ATLAS_API_KEY)
		res_id_1 = [27151070]
		res_id_2 = [27151071]
		# print("Waiting 15mins for Ripe results...")
		# time.sleep(900)
		# if len(res_id_1)!=0:
		# 	fetch_ripe_result(res_id_1[0], "website_1_trace.txt")
		# else:
		# 	print("Results for", website_1,"could not be fetched")

		# if len(res_id_2)!=0:
		# 	fetch_ripe_result(res_id_2[0], "website_2_trace.txt")
		# else:
		# 	print("Results for", website_2,"could not be fetched")


		find_cdns("website_1_trace.txt")
		find_cdns("website_2_trace.txt")
		



		# #---------USE TRACEROUTE AND GEOLITE GEOLOCATION TOO FIND THE SERVERS--------
		# process = subprocess.run(["tracert", website_1], shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
		# output = process.stdout
		# print(output)
		# print("")
		# process = subprocess.run(["tracert", website_2], shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
		# output = process.stdout
		# print(output)


   		#------------USE RIPE ATLAS FOR TRACEROUTE MEASUREMENTS-----------------
		

		

		
				
			#time.sleep(30)

	else:
		print("usage: protocol_analysis <website_1> <website_2>")


if __name__ == "__main__":
	main(sys.argv)
