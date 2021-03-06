import xml.etree.ElementTree as ET
import os.path

class XML_Handler:

	def find_xml(xml_path=""):
		# if path has content, verify it then return
		if xml_path != "":
			if os.path.isfile(xml_path) == True:
				return xml_path
			else:
				exit("Path to application.xml file is invalid, check the path and try again.")
		# if path = "" look for "application.xml" in working dir and in "./application-properties/"
		else:
			if os.path.isfile('./application-properties/application.xml') == True:
				xml_path = "./application-properties/application.xml"
			elif os.path.isfile('./application.xml') == True:
				xml_path = "./application.xml"
			return xml_path

	def parse_env(xml_path):
		app_xml = ET.parse(xml_path)
		app_xml_root = app_xml.getroot()
		product = app_xml_root.find('product').attrib.get('name')
		if product.lower() == 'bitbucket':
			build_number = app_xml_root.find('bitbucket-information').find('build-number').text  # returns string like 6002001 (6.2.1)
			# ^^ needs to be revised to support non-bitbucket applications
			temp = app_xml_root.findall('cluster-information')
			if len(temp) > 1: # if clustering is in use, first "cluster-information" lists the nodes in the cluster
				dc = "true"
			else: # if 1 node is in use, still check to see if clustering might be allowed
				dc = temp[0].find('clustering-available').text
				#print("Product: ",product, ",  Build_number: ",build_number, ",  DataCenter: ", dc)
		elif product.lower() == 'confluence':
			build_number = app_xml_root.find('application-information').find('build-number').text
			clusternode = app_xml_root.findall('cluster-information')
			if (len(clusternode) > 0):
				dc = True
			else:
				dc = False
		# add elif for jira, fecru, bamboo... etc.
		return [product,build_number,dc]


	def parse_plugins(xml_path):
		app_xml = ET.parse(xml_path) # change to variable "input_xml" 
		print("Parsing plugins...")
		plugins = app_xml.find('plugins')
		for plugin in plugins.iter('plugin'):
			key = plugin.find('key').text
			try:
				name = plugin.find('name').text
			except: #failover for older application.xmls where no name is stored.
				name = key
			version = plugin.find('version').text.split('-')[0]
			status = plugin.find('status').text
			try:
				bundled = plugin.find('bundled').text
			except:
				bundled = "unknown"
				'''
				failover for older application.xmls where no 'bundled' attribute is stored. 
				This will cause all plugins to be checked rather than non-'bundled' causing longer processing time.
				'''
			#print(key, name, version, status, bundled)
			yield [key,name,version,status,bundled]
