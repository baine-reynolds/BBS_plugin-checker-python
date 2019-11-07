from resources.xml_handler import XML_Handler
from resources.init import Init
import concurrent.futures

class Source_Environment:
	def __init__(self, application_info):
		self.product = application_info[0]
		self.version = application_info[1]
		self.dc = application_info[2]



def parse_check(proposed_path):
	# prep executor for threading
	executor = concurrent.futures.ThreadPoolExecutor()
	# init empty list for threads
	tasks = []
	# verify path provided by flag "-f" 
	xml_path = XML_Handler.find_xml(proposed_path)
	env = XML_Handler.parse_env(xml_path)
	print(env)    # for testing
	for plugin in XML_Handler.parse_plugins(xml_path):
		print(plugin)    # for testing
		# prep thread for each plugin
		#future = executor.submit(web_scrap, env, plugin)
		# start thread
		#tasks.append(future)
	#concurrent.futures.wait(tasks)

def main():
	options, args = Init.parse_input()
	output = parse_check(options.filepath)
	#formated_output = 
	#output()
	exit("Complete")

if __name__ == "__main__":
    main()