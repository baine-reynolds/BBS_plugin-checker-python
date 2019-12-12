from colorama import Fore, Style

class Formatter:
	def format(disabled_bundled, raw_apps, env, markdown):
		not_compatible = []
		not_compatible_latest = []
		not_latest = []
		latest = []
		unknown = [] # Will likely consist of "Provided" status plugins
		for app in raw_apps:
			if app[0] == "unknown":
				unknown.append(app)
			elif app[0] == "incompatible" and app[5] == False:
				not_compatible.append(app)
			elif app[0] == "incompatible" and app[5] == True: #incompatible, but running the latest release possible meaning that upgrading isn't possible
				not_compatible_latest.append(app)
			elif app[0] == "compatible_old":
				not_latest.append(app)
			else: # compatible and latest
				latest.append(app)
		# Need to add feature to mark if plugin is disabled or not. 
		if markdown:
			print("{panel:title=Plugin compatibility for " + env.product + " on version " + env.version + "}")
			markdown_setup_line = "||Plugin Name||Plugin Key||Plugin Version||"
			if len(not_compatible) > 0:
				print("\nh3. The following Plugins are installed but NOT COMPATIBLE with your current version of " + 
					env.product + ": " + env.version)
				print(markdown_setup_line)
				for app in not_compatible:
					print("|{color:red}" + app[2] + "{color}|{color:red}" + app[1] + "{color}|{color:red}" + app[3] + "{color}|")
			if len(not_compatible_latest) > 0:
				print("\nh3. The following Plugins are installed but NOT COMPATIBLE with your current version of " + 
					env.product + ": " + env.version + ", however, there are no newer releases. We recommend disabling these plugins and finding alternatives.")
				print(markdown_setup_line)
				for app in not_compatible_latest:
					print("|{color:red}" + app[2] + "{color}|{color:red}" + app[1] + "{color}|{color:red}" + app[3] + "{color}|")
			if len(not_latest) > 0:
				print("\nh3. The following Plugins are COMPATIBLE with your current version of " + 
					env.product + " but are NOT running the latest version. " + "Consider upgrading at your earliest convenience.")
				print(markdown_setup_line)
				for app in not_latest:
					print("|{color:orange}" + app[2] + "{color}|{color:orange}" + app[1] + "{color}|{color:orange}" + app[3] + "{color}|")
			if len(latest) > 0:
				print("\nh3. The following Plugins are installed and Up to Date:")
				print(markdown_setup_line)
				for app in latest:
					print("|{color:green}" + app[2] + "{color}|{color:green}" + app[1] + "{color}|{color:green}" + app[3] + "{color}|")
			if len(unknown) > 0:
				print("\nh3. The following Plugins were not identified in the marketplace, " + 
					"meaning that they are likely in-house custom plugins, system plugins, or the version number could not be parsed successfully.")
				print(markdown_setup_line)
				for app in unknown:
					print("|{color:grey}" + app[2] + "{color}|{color:grey}" + app[1] + "{color}|{color:grey}" + app[3] + "{color}|")
			if len(disabled_bundled) > 0:			
				print("\nh3. The following are Apps that are apart of Bitbucket itself that are currently disabled." + 
					"\nWe Highly recommend re-enableing these apps.")
				for app in disabled_bundled:
					print("{color:red}" + app + "{color}")
			print("{panel}")
		else:
			print("Plugin compatibility for " + env.product + " on version " + env.version)
			if len(not_compatible) > 0:
				print("\nThe following Plugins are installed but NOT COMPATIBLE with your current version of " + 
					env.product + ": " + env.version)
				for app in not_compatible:
					print(Fore.RED + "  Name:" + app[2] + "   Key:" + app[1] + "   Current Version:" + app[3] + Style.RESET_ALL)
			if len(not_compatible_latest) > 0:
				print("\nThe following Plugins are installed but NOT COMPATIBLE with your current version of " + 
					env.product + ": " + env.version + ", however, there are no newer releases. We recommend disabling these plugins and finding alternatives.")
				for app in not_compatible_latest:
					print(Fore.RED + "  Name:" + app[2] + "   Key:" + app[1] + "   Current Version:" + app[3] + Style.RESET_ALL)
			if len(not_latest) > 0:
				print("\nThe following Plugins are COMPATIBLE with your current version of " +
					env.product + " but are NOT running the latest version. Consider upgrading at your earliest convenience.")
				for app in not_latest:
					print(Fore.YELLOW + "  Name:" + app[2] + "   Key:" + app[1] + "   Current Version:" + app[3] + Style.RESET_ALL)
			if len(latest) > 0:
				print("\nThe following Plugins are installed and up to date:")
				for app in latest:
					print(Fore.GREEN + "  Name:" + app[2] + "   Key:" + app[1] + "   Current Version:" + app[3] + Style.RESET_ALL)
			if len(unknown) > 0:
				print("\nThe following Plugins were not identified in the marketplace, " + 
					"meaning that they are likely in-house custom plugins, system plugins, or the version number could not be parsed successfully.")
				for app in unknown:
					print(Fore.WHITE + "  Name:" + app[2] + "   Key:" + app[1] + "   Current Version:" + app[3] + Style.RESET_ALL)
			if len(disabled_bundled) > 0:			
				print("\nThe following are Apps that are apart of Bitbucket itself that are currently disabled." + 
					"\nWe Highly recommend re-enableing these apps.")
				for app in disabled_bundled:
					print(Fore.RED + app + Style.RESET_ALL)
