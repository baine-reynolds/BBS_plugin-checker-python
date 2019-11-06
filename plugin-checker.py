
class Source_Environment:
	def __init__(self, application_info):
		self.product = application_info[0]
		self.version = application_info[1]
		self.dc = application_info[2]

class Script_actions():
	def check_plugin(environment, plugin):




# read application.xml
def read_app_xml():
	pass
	# find properties values first and send to 
	# for each "<plugin>" to "</plugin>" section found, spin up a new thread



# build list "application_info" and dictionary "plugin_info"
#	application-info = [product-name (bitbucket/crowd/fecru/jira/etc...), product-version, DC?]
#		# Bitbucket if DC or not <clustering-available>true</clustering-available>  (false if server)
#	plugin-info = {plugin_key: [name, version, vendor, status, vendor-url, framework-version, bundled]}
#		# bundled = "Bundled" or "User installed"



# init "Source-Environment" class
server = Source_Environment()
# populate class values
server.product
for plugin in plugin-info:
	thread-out(check_plugin(server, plugin))

def main():
	read_app_xml()
	format_output()
	output()
	exit("Complete")

if __name__ == "__main__":
    main()