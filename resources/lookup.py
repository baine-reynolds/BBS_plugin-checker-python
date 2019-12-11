import requests
import re

class Marketplace:
	def lookup(env,plugin, paged_start=None, paged_limit=None, gathering_plugin_data = True):
		while gathering_plugin_data:
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
				r_data = r.json()
				plugin_uri = r_data['_links']['alternate']['href']
				plugin_url = marketplace_Url + plugin_uri.replace('/version-history', '')
				
				for version in r_data['_embedded']['versions']:
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
			#if r_data['isLastPage'] == True:
			gathering_plugin_data = False
			#paged_start = r_data['nextPageStart']
		temp_results, latest_possible = Marketplace.compare(env,plugin,all_versions)
		results = [temp_results, plugin.key, plugin.name, plugin.version, plugin.status, latest_possible]
		return(results)

	def latest_check(plugin):
		# Check to see if regardless of env, if the plugin located in app.xml is running the latest release possible.
		marketplace_Url = "https://marketplace.atlassian.com"
		api_endpoint = "/rest/2/addons/"+plugin.key+"/versions/latest"
		r = requests.get(marketplace_Url+api_endpoint)
		r_data = r.json()
		latest_version = r_data['name']
		if latest_version in plugin.version:
			latest = True
		else:
			latest = False
		return latest

	def compare(env,plugin,all_versions):
		# compatibility types = compatible_latest, compatible_old, incompatible, unknown
		if len(all_versions) > 0:
			# convert actual plugin version to full build number
			actual_plugin_version = Marketplace.clean_individual(plugin.version)
			# create a list of full build numbers from the returned decimal version numbers to compare against
			plugin_build_versions = []
			for version in all_versions:
				version_cleaned = Marketplace.clean_individual(version[0])
				plugin_build_versions.append(version_cleaned)
			if actual_plugin_version == max(plugin_build_versions):
				compatibility = "compatible_latest"
				latest_possible = True
			else:
				compatibility = "compatible_old"
				latest_possible = False
		else:  # no compatible versions found, aka incompatible
			compatibility = "incompatible"
			latest_possible = Marketplace.latest_check(plugin)
		return compatibility, latest_possible

	def clean_individual(option):
		option_numbers = re.sub("[A-z]", "", option).strip(" ").split("-")
		split = option_numbers[0].split(".")
		multiplier = 1000000000
		version = 0
		for num in split:
			version += int(num) * multiplier
			multiplier = multiplier / 1000
		return int(float(version))
