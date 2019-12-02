from colorama import Fore, Style

class Formatter:
	def format(disabled_bundled, raw_apps, env):
		print("Plugin compatibility for",env.product,"on version",env.version)
		not_compatible = []
		not_latest = []
		latest = []
		unknown = [] # Will likely consist of "Provided" status plugins
		for app in raw_apps:
			if app[0] == "unknown":
				unknown.append(app)
			elif app[0] == "incompatible":
				not_compatible.append(app)
			elif app[0] == "compatible_old":
				not_latest.append(app)
			else:
				latest.append(app)
		# Need to add feature to mark if plugin is disabled or not. 
		if len(not_compatible) > 0:
			print("\nThe following Plugins are installed but NOT COMPATIBLE with your current version of ",
				env.product, ": ",env.version)
			for app in not_compatible:
				print(Fore.RED,"  Name:",app[2],"   Key:",app[1],"   Current Version:",app[3],Style.RESET_ALL)
		if len(not_latest) > 0:
			print("\nThe following Plugins are COMPATIBLE with your current version of ",
				env.product, " but are NOT running the latest version. ",
				"Consider upgrading at your earliest convenience.")
			for app in not_latest:
				print(Fore.YELLOW,"  Name:",app[2],"   Key:",app[1],"   Current Version:",app[3],Style.RESET_ALL)
		if len(latest) > 0:
			print("\nThe following Plugins are installed and Up to Date:")
			for app in latest:
				print(Fore.GREEN,"  Name:",app[2],"   Key:",app[1],"   Current Version:",app[3],Style.RESET_ALL)
		if len(unknown) > 0:
			print("\nThe following Plugins were not identified in the marketplace, ",
				"meaning that they are likely in-house custom plugins, system plugins, or the version number could not be parsed successfully.")
			for app in unknown:
				print(Fore.WHITE,"  Name:",app[2],"   Key:",app[1],"   Current Version:",app[3],Style.RESET_ALL)
		if len(disabled_bundled) > 0:			
			print("The following are Apps that are apart of Bitbucket itself that are currently disabled.",
				"\nWe Highly recommend re-enableing these apps.")
			for app in disabled_bundled:
				print(Fore.RED,app,Style.RESET_ALL)