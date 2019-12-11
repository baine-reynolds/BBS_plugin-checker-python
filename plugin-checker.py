from resources.init import Init
from resources.xml_handler import XML_Handler
from resources.format_output import Formatter
from resources.lookup import Marketplace
import concurrent.futures

__author__ = "Michael Walker"
__maintainer__ = "Michael Walker"
__email__ = "michaelchwalker@gmail.com"

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
	disabled_bundled = []
	user_installed_plugin = []
	for item in XML_Handler.parse_plugins(xml_path):
		plugin = Plugin(item)
		if plugin.bundled.lower() == "bundled":
			if plugin.status.lower() == "installed" or plugin.status.lower() == "disabled":
				disabled_bundled.append(plugin.key)
		else:
			user_installed_plugin.append(plugin.key)
			# start new thread
			tasks.append(executor.submit(Marketplace.lookup,environment,plugin))
	# wait for all threads to complete before proceeding
	to_format = []
	print("Performing Marketplace lookups for each plugin...")
	for f in concurrent.futures.as_completed(tasks):
		to_format.append(f.result())
	return disabled_bundled, to_format, environment


def main():
	options, args = Init.parse_input()
	disabled_bundled, raw_format, env = parse_check(options.filepath)
	Formatter.format(disabled_bundled, raw_format, env, options.markdown)
	exit()

if __name__ == "__main__":
	main()
