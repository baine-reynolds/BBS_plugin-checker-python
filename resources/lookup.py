import requests
from bs4 import BeautifulSoup as bs
import re

class Marketplace:
	def lookup(env,plugin):
		marketplace_Url = "https://marketplace.atlassian.com"
		# web scrape the marketplace to find and validate the plugin
		# curl for https://marketplace.atlassian.com/rest/2/addons/<plugin.key>
		curl = requests.get(marketplace_Url+"/rest/2/addons/"+str(plugin.key))
		if curl.status_code == 404:
			results = ["unknown", plugin.key, plugin.version, env.product, env.version]
		else: # plugin found in marketplace
			# parse for "_links"."alternate"."href" and remove "?tab=overview"
			endpoint = curl.json()['_links']['alternate']['href']
			endpoint_cleaned = endpoint.split('?')[0]
			# resulting in "/apps/<app-id>/<package-name>"
			# take new string and enter in https://atlassian.marketplace.com/<result_string>/version-history
			raw_page = requests.get(marketplace_Url+"/"+str(endpoint_cleaned)+"/version-history")
			# parse results
			page = bs(raw_page.text, 'html.parser')
			version_history = page.find(class_='plugin-versions')
			all_versions = []
			for version in version_history.find_all('li'):
				number = version.find(class_='version')
				compatibility = version.find(class_='compatible-apps')
				#for spsn in version_compatibility:
				#	version_compatibility = version_compatibility.find_all(class_='application').contents
				if version == None or compatibility == None:
					pass
				else:
					version_number = str(number.contents).strip("[]'`")
					version_compatibility = str(compatibility.contents).strip("[]'").replace('<span class="application">','').replace("</span>","").replace(" ',', <br/>, ","").replace("<br>","").replace("</br>","").split(',')
					for product in version_compatibility:
						if "bitbucket" in product.lower():
							relevant_compatibility = product
					all_versions.append([version_number, relevant_compatibility])
			results = Marketplace.compare(env,plugin,all_versions)
		return(results)


	def compare(env,plugin,all_versions):
		compatibility = "checked" # compatible_latest, compatible_old, incompatible, unknown
		for env_version, actual_plugin_version, checked_plugin_version, version_minimum, version_maximum in Marketplace.parse_versions(env, plugin, all_versions):
			pass
			# work here next
#			print("env, plugin, min, max")
#			print(env_version)
#			print(actual_plugin_version)
#			print(checked_plugin_version)
#			print(version_minimum)
#			print(version_maximum)
		# compatible and current
		# compatible but not latest
		# not-compatible
		return([compatibility, plugin.key, plugin.version, env.product, env.version])

	def parse_versions(env,plugin,all_versions):
		dc_versions = []
		server_versions = []
		env_version = Marketplace.clean_individual(env.version)
		actual_plugin_version = Marketplace.clean_individual(plugin.version)
		for option in all_versions:
			if "data center" in option[1].lower():
				dc_versions.append(option)
			else:
				server_versions.append(option)
		if env.dc == "true":
			for option in dc_versions:
				checked_plugin_version = Marketplace.clean_individual(option[0])
				version_minimum, version_maximum = Marketplace.clean_ranges(option[1])
				yield env_version, actual_plugin_version, checked_plugin_version, version_minimum, version_maximum
		else:
			for option in server_versions:
				checked_plugin_version = Marketplace.clean_individual(option[0])
				version_minimum, version_maximum = Marketplace.clean_ranges(option[1])
				yield env_version, actual_plugin_version, checked_plugin_version, version_minimum, version_maximum
		# example: ['5.3.0', 'Bitbucket Data Center 5.2.0 - 6.8.0']

	def clean_ranges(option):
		# converts version numbers from 6.1.12 to 6001012 (6,001,012) for ease of comparing versions
		option_numbers = re.sub("[A-z]", "", option).strip(" ").split("-")
		if len(option_numbers) == 1:
			compatible_split = option_numbers[0].split(".")
			compatible_multiplier = 1000000000
			compatible_version = 0
			for num in compatible_split:
				compatible_version += int(num) * compatible_multiplier
				compatible_multiplier = int(compatible_multiplier) / 1000
			return int(float(compatible_version)), int(float(compatible_version))
		elif len(option_numbers) == 2:
			min_split = option_numbers[0].split(".")
			min_multiplier = 1000000000
			min_version = 0
			for num in min_split:
				min_version += int(num) * min_multiplier
				min_multiplier = int(min_multiplier) / 1000
			max_split = option_numbers[1].split('.')
			max_multiplier = 1000000000
			max_version = 0
			for num in max_split:
				max_version += int(num) * int(max_multiplier)
				max_multiplier = int(max_multiplier) / 1000
			return int(float(min_version)), int(float(max_version))

	def clean_individual(option):
		option_numbers = re.sub("[A-z]", "", option).strip(" ").split("-")
		if len(option_numbers) == 1:
			split = option_numbers[0].split(".")
			multiplier = 1000000000
			version = 0
			for num in split:
				version += int(num) * multiplier
				multiplier = int(multiplier) / 1000
			return int(float(version))