class Marketplace:
	def lookup(env,plugin):
		print("Name: " + str(plugin.name) + "\nBundled: " + str(plugin.bundled))
		# web scrape the marketplace to find and validate the plugin