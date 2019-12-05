from optparse import OptionParser

class Init:
	def parse_input():
		parser = OptionParser()
		parser.add_option('-f', '--file', dest='filepath', help="Path to application.xml file", metavar="FILE")
		parser.add_option('-m', '--markdown', dest='markdown', default=False, action="store_true", help="Output in Markdown for direct pasting into Jira")
		options, args = parser.parse_args()
		return options, args