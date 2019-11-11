class Formatter:
	def format(disabled_bundled, raw_apps, env):
		not_compatible = []
		not_latest = []
		latest = []
		unknown = []
		for app in raw_apps:
			if app[0] == "unknown":
				unknown.append(app)
			elif app[0] == "incompatible":
				not_compatible.append(app)
			elif app[0] == "compatible_old":
				not_latest.append(app)
			else:
				latest.append(app)
		if len(not_compatible) > 0:
			print("The following Plugins are installed but not compatible with your current version of ",
				env.product, ": ",env.version)
			for app in not_compatible:
				print("  Name: ",app[2],"  Key: ",app[1],"  Current Version: ",app[3])
		if len(not_latest) > 0:
			print("\nThe following Plugins are compatible with your current version of ",
				env.product, " but are not running the lastest version. ",
				"Consider upgrading at your earliest convenience.")
			for app in not_latest:
				print("  Name: ",app[2],"  Key: ",app[1],"  Current Version: ",app[3])
		if len(latest) > 0:
			print("\nThe following Plugins are installed and Up to Date:")
			for app in latest:
				print("  Name: ",app[2],"  Key: ",app[1],"  Current Version: ",app[3])
		if len(disabled_bundled) > 0:			
			print("The following are Apps that are apart of Bitbucket itself that are currently disabled.",
				"\nWe Highly recommend re-enableing these apps.")
			for app in disabled_bundled:
				print(app)