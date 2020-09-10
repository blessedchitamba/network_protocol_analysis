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

def main(argv):
	website_1 = ''
	website_2 = ''
	ATLAS_API_KEY = "9b81eb94-44fe-4e2e-aca7-508b94b7041b"
	if len(sys.argv)==3:
		website_1 = sys.argv[1]
		website_2 = sys.argv[2]
		myResolver = dns.resolver.Resolver()

		#start with the nameservers of each website
		print(website_1, "has the following nameservers:")
		try:
			result = myResolver.resolve(website_1, 'NS')
			for nameserver in result:
				print('nameserver:', nameserver.to_text())
		except:
			print("There was an error...")

		print("")
		print(website_2, "has the following nameservers:")
		try:
			result = myResolver.resolve(website_2, 'NS')
			for nameserver in result:
				print('nameserver:', nameserver.to_text())
		except:
			print("There was an error...")


		#check for ipv4
		print("Checking for ipv4 support in",website_1,":")
		try:
			result = myResolver.resolve(website_1, 'A')
			for ipv4 in result:
				print('ipv4:', ipv4.to_text())
		except:
			print("There was an error...")

		print("")
		print("Checking for ipv4 support in",website_2,":")
		try:
			result = myResolver.resolve(website_2, 'A')
			for ipv4 in result:
				print('ipv4:', ipv4.to_text())
		except:
			print("There was an error...")

		#check for ipv6 support
		print("Checking for ipv6 support in",website_1,":")
		try:
			result = myResolver.resolve(website_1, 'AAAA')
			for ipv6 in result:
				print('ipv6:', ipv6.to_text())
		except:
			print("There was an error...")

		print("")
		print("Checking for ipv6 support in",website_2,":")
		try:
			result = myResolver.resolve(website_2, 'AAAA')
			for ipv6 in result:
				print('ipv6:', ipv6.to_text())
		except:
			print("There was an error...")



		# #---------USE TRACEROUTE AND GEOLITE GEOLOCATION TOO FIND THE SERVERS--------
		# process = subprocess.run(["tracert", website_1], shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
		# output = process.stdout
		# print(output)
		# print("")
		# process = subprocess.run(["tracert", website_2], shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
		# output = process.stdout
		# print(output)


   		#------------USE RIPE ATLAS FOR TRACEROUTE MEASUREMENTS-----------------
		traceroute1 = Traceroute(
			af=4,
			target=website_1,
			description="testing",
			protocol="ICMP",
		)

		source1 = AtlasSource(
			type="country",
			value="CA", #, canada "CA", "PL", "AU", "AR"],
			requested=20,
			tags={"include":["system-ipv4-works"]}
		)

		source2 = AtlasSource(
			type="country",
			value="ZA", #, South Africa "CA", "PL", "AU", "AR"],
			requested=10,
			tags={"include":["system-ipv4-works"]}
		)

		source3 = AtlasSource(
			type="country",
			value="DE", #, Germany "CA", "PL", "AU", "AR"],
			requested=20,
			tags={"include":["system-ipv4-works"]}
		)

		source4 = AtlasSource(
			type="country",
			value="NG", #, Nigeria "CA", "PL", "AU", "AR"],
			requested=20,
			tags={"include":["system-ipv4-works"]}
		)

		source5 = AtlasSource(
			type="country",
			value="BR", #, Brazil "CA", "PL", "AU", "AR"],
			requested=20,
			tags={"include":["system-ipv4-works"]}
		)

		atlas_request = AtlasCreateRequest(
			start_time=datetime.utcnow(),
			key=ATLAS_API_KEY,
			measurements=[traceroute1],
			sources= [source1, source2, source3, source4, source5],
			is_oneoff=True
		)

		# (is_success, response) = atlas_request.create()
		# result_id = []
		# if is_success:
		# 	result_id = response['measurements']
		# 	print(result_id)
		# else:
		# 	print("Measurement not successful")

		# #fetch the result
		# kwargs = {
		# 	"msm_id": result_id[0],
		# }

		# time.sleep(300)

		# not_fetched = True
		# print("Waiting for Ripe results...")
		# while not_fetched:
		# 	is_success, results = AtlasResultsRequest(**kwargs).create()
		# 	if len(results)!=0:
		# 		not_fetched = False
		# 		print(len(results))
		# 		for res in results:
		# 			print("Source address: ",res['src_addr'])
		# 			result_size = len(res['result'])
		# 			print("Destination address: ",res['result'][result_size-1]['result'][1]['from'])
		# 			print("")
		# 		s = "traceroute.txt"
		# 		with open(s, 'w') as outfile:
		# 			json.dump(results, outfile)

		
				
			#time.sleep(30)

	else:
		print("usage: protocol_analysis <website_1> <website_2>")


if __name__ == "__main__":
	main(sys.argv)
