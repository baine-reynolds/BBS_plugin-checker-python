from optparse import OptionParser

class Init:
	def parse_input():
		parser = OptionParser()
		parser.add_option('-f', '--file', dest='filepath', help="Path to application.xml file", metavar="FILE")
		#parser.add_option('-q', '--quiet', action='count', dest='quiet', default=0, help="Decreases verbosity.")
		options, args = parser.parse_args()
		return options, args