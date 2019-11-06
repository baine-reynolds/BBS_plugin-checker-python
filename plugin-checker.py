from resources.xml_handler import XML_Handler

class Source_Environment:
	def __init__(self, application_info):
		self.product = application_info[0]
		self.version = application_info[1]
		self.dc = application_info[2]

class Script_actions():
	def check_plugin(environment, plugin):
		pass

def main():
	env = XML_Handler.parse_env()
	print(env)
	print("----------")
	for plugin in XML_Handler.parse_plugins():
		print(plugin)
	#format_output()
	#output()
	exit("Complete")

if __name__ == "__main__":
    main()