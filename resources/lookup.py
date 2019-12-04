import requests
from bs4 import BeautifulSoup as bs
import re

class Marketplace:
	def lookup_old(env,plugin):
		marketplace_Url = "https://marketplace.atlassian.com"
		# web scrape the marketplace to find and validate the plugin
		curl = requests.get(marketplace_Url+"/rest/2/addons/"+str(plugin.key))
		if curl.status_code == 404:
			results = ["unknown", plugin.key, plugin.name, plugin.version, plugin.status]
		else: # plugin found in marketplace
			# parse for "_links"."alternate"."href" and remove "?tab=overview"
			endpoint = curl.json()['_links']['alternate']['href']
			endpoint_cleaned = endpoint.split('?')[0]
			# resulting in "/apps/<app-id>/<package-name>"
			raw_page = requests.get(marketplace_Url+"/"+str(endpoint_cleaned)+"/version-history")
			page = bs(raw_page.text, 'html.parser')
			version_history = page.find(class_='plugin-versions')
			all_versions = []
			for version in version_history.find_all('li', 'version-row'):
				try:
					version_number = version.find(class_='version').get_text()
				except:
					version_number = None #broken li object listing
				try:
					version_compatibility = version.find(class_='compatible-apps').get_text().split(',')
				except:
					version_compatibility = None
				if version_number == None or version_compatibility == None:
					pass #broken li object gathered, dumping results
				else:
					for product in version_compatibility:
						if env.product.lower() in product.lower():
							relevant_compatibility = product
					all_versions.append([version_number, relevant_compatibility])
			results = Marketplace.compare(env,plugin,all_versions)
		return(results)






	def lookup(env,plugin, paged_start=None, paged_limit=None):
		results = []
		while True:
			marketplace_Url = "https://marketplace.atlassian.com"
			versions_endpoint = "/rest/2/addons/"+plugin.key+"/versions"
			params = {'application': env.product.lower(), 'applicationBuild': env.version, 'start': paged_start, 'limit': paged_limit}
			headers = {'X-Atlassian-Token': 'nocheck', "Content-Type": "application/json", "Accept": "application/json"}
			all_versions = []
			r = requests.get(marketplace_Url+versions_endpoint, params=params, headers=headers)
			if r.status_code == 404:
				results = ["unknown", plugin.key, plugin.name, plugin.version, plugin.status]
				return(results)
			else: # plugin found in marketplace
				plugin_uri = r.json()['_links']['alternate']['href']
				plugin_url = marketplace_Url + plugin_uri.replace('/version-history', '')
				for version in r.json()['_embedded']['versions']:
					version_number = version['name']
					if version['deployment']['server'] == True and version['deployment']['dataCenter'] == True:
						product_compatibility = "both"
					elif version['deployment']['server'] == True and version['deployment']['dataCenter'] == False:
						product_compatibility = "server"
					elif version['deployment']['server'] == False and version['deployment']['dataCenter'] == True:
						product_compatibility = "dataCenter"
					else:
						product_compatibility = "server"
						print("Defaulting to 'Server' compatibility as no plugin product details could be found.")
					all_versions.append([version_number, product_compatibility])
				results.append(Marketplace.compare(env,plugin,all_versions))
			if r_data['isLastPage'] == True:
				return(results)
			paged_start = r_data['nextPageStart']

	def compare(env,plugin,all_versions):
		compatibility = "checked" # compatible_latest, compatible_old, incompatible, unknown
		compatible_versions = []
		compatible = False
		for env_version, actual_plugin_version, checked_plugin_version, version_minimum, \
			version_maximum in Marketplace.parse_versions(env, plugin, all_versions):
			if int(env_version) in range(version_minimum, version_maximum):
				compatible = True
				compatible_versions.append(checked_plugin_version)
		latest = True
		for version in compatible_versions:
			if int(actual_plugin_version) < int(version):
				latest = False
		if compatible == True and latest == True:
			compatibility = "compatible_latest"
		elif compatible == True and latest == False:
			compatibility = "compatible_old"
			# consider adding a "max(compatible_versions)" to return the actual "latest"
		else: 
			compatibility = "incompatible"
		return([compatibility, plugin.key, plugin.name, plugin.version, plugin.status])

	def parse_versions(env,plugin,all_versions):
		dc_versions = []
		server_versions = []
		env_version = Marketplace.clean_individual(env.version)
		actual_plugin_version = Marketplace.clean_individual(plugin.version)
		for option in all_versions:
			if "datacenter" in option[1].lower():
				dc_versions.append(option)
			else:
				server_versions.append(option)
		if env.dc == "true" and len(dc_versions) > 0:
			for option in dc_versions:
				checked_plugin_version = Marketplace.clean_individual(option[0])
				version_minimum, version_maximum = Marketplace.clean_ranges(option[1])
				yield env_version, actual_plugin_version, checked_plugin_version, \
					version_minimum, version_maximum
		else: #check if a "server" version is available
			for option in server_versions:
				checked_plugin_version = Marketplace.clean_individual(option[0])
				version_minimum, version_maximum = Marketplace.clean_ranges(option[1])
				yield env_version, actual_plugin_version, checked_plugin_version, \
					version_minimum, version_maximum
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
				compatible_multiplier = compatible_multiplier / 1000
			return int(float(compatible_version)), int(float(compatible_version))
		elif len(option_numbers) == 2:
			min_split = option_numbers[0].split(".")
			min_multiplier = 1000000000
			min_version = 0
			for num in min_split:
				min_version += int(num) * min_multiplier
				min_multiplier = min_multiplier / 1000
			max_split = option_numbers[1].split('.')
			max_multiplier = 1000000000
			max_version = 0
			for num in max_split:
				max_version += int(num) * max_multiplier
				max_multiplier = max_multiplier / 1000
			return int(float(min_version)), int(float(max_version))

	def clean_individual(option):
		option_numbers = re.sub("[A-z]", "", option).strip(" ").split("-")
		if len(option_numbers) == 1:
			split = option_numbers[0].split(".")
			multiplier = 1000000000
			version = 0
			for num in split:
				version += int(num) * multiplier
				multiplier = multiplier / 1000
			return int(float(version))