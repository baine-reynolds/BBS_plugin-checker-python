from resources.init import Init
from resources.xml_handler import XML_Handler
from resources.format_output import Formatter
from resources.lookup import Marketplace
import concurrent.futures

class Source_Environment:
	def __init__(self, application_info):
		self.product = application_info[0]
		self.version = application_info[1]
		self.dc = application_info[2]

class Plugin:
	def __init__(self, plugin_info):
		self.key = plugin_info[0]
		self.name = plugin_info[1]
		self.version = plugin_info[2]
		self.status = plugin_info[3]
		self.bundled = plugin_info[4]

def parse_check(proposed_path):
	# prep executor for threading
	executor = concurrent.futures.ThreadPoolExecutor()
	# init empty list for threads
	tasks = []
	# verify path provided by flag "-f" 
	xml_path = XML_Handler.find_xml(proposed_path)
	application_info = XML_Handler.parse_env(xml_path)
	environment = Source_Environment(application_info)
	all_plugins = []
	bundled_plugin = []
	user_installed_plugin = []
	for item in XML_Handler.parse_plugins(xml_path):
		plugin = Plugin(item)
		all_plugins.append(plugin.key)
		if plugin.bundled.lower() == "bundled":
			bundled_plugin.append(plugin.key)
		else:
			user_installed_plugin.append(plugin.key)
			# prep thread for each plugin
			future = executor.submit(Marketplace.lookup, environment, plugin)
			# start new thread
			tasks.append(future)
	# wait for all threads to complete before completing
	concurrent.futures.wait(tasks)

def main():
	options, args = Init.parse_input()
	raw_output = parse_check(options.filepath)
	clean_output = Formatter.format(raw_output)
	exit("Complete")

if __name__ == "__main__":
    main()