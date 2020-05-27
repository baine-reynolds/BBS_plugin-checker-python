# Usage:
Run the "plugin-checker.py" file pointed at an application.xml file from a Bitbucket support zip to quickly check all plugins to check if plugins are compatible or not.

        python3 plugin-checker.py -f /path/to/application.xml

You can also add the "-m" flag at the end to set markdown formatting to be copied directly into Jira or Confluence.

        python3 plugin-checker.py -f /path/to/application.xml -m

# Dependencies:
* [Python3](https://www.python.org/downloads/) This was written in python3.7 and requires at least 3.5+ to operate as expected.
* [Requests](http://docs.python-requests.org/en/master/)

        pip3 install requests --user

* [Colorama](https://pypi.org/project/colorama/)

        pip3 install colorama --user
