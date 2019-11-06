import xml.etree.ElementTree as ET

class XML_Handler:

	def parse_env():
		app_xml = ET.parse('application.xml')
		product = app_xml.find('product').attrib.get('name')
		version = app_xml.find('product').attrib.get('version')
		dc = app_xml.find('cluster-information').find('clustering-available').text
		return [product,version,dc]

	def parse_plugins():
		app_xml = ET.parse('application.xml') # change to variable "input_xml" 
		plugins = app_xml.find('plugins')
		for plugin in plugins.iter('plugin'):
			key = plugin.find('key').text
			name = plugin.find('name').text
			version = plugin.find('version').text
			status = plugin.find('status').text
			bundled = plugin.find('bundled').text
			plugin_details = [key,name,version,status,bundled]
			yield plugin_details