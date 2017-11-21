import re

url = 'http://www.oldversion.com/windows/mw-virtual-destop-0-2-8-2'
after_last_slash=url.split("/")[-1]
str=after_last_slash

# Thanks to https://stackoverflow.com/a/26445549 for the "cannot start with 0" example :)
match = re.match(r'^([a-z-]+)(?!\d)', str, re.IGNORECASE)

#folder_name=

# test if search() found a match
if match:
	print('found: \'' + match.group(1) + '\'')
else:
	print('did not find')