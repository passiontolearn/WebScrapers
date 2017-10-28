import rfc6266, requests  # for getting filename from content-disposition
import os, re
from pySmartDL import SmartDL
from robobrowser import RoboBrowser

DEBUG = False	# Set to True for debug print statements
def _debug_print(s):
    if DEBUG:
        print(s)

''' We want for example to get 'mw-virtual-desktop'
	from: http://www.oldversion.com/windows/mw-virtual-desktop-0-2-8-2
'''
folder_regex = re.compile(r'^([a-z-]+)(?!\d)', re.IGNORECASE)  # Using (?!d) enables us to not match a number
def get_foldername_from_url(url):
	after_slash = url.split("/")[-1] # get the part of the *last* slash
	match = folder_regex.match(after_slash)
	foldername = match.group(1)
	if match:
		_debug_print('found foldername: \'' + match.group(1) + '\' for URL: ' + url)
	else:
		print('WARNING: could not find a foldername for URL: ' + url)
	return foldername

prevFolderName = " "
def update_prevFolderName(folderName):
	global prevFolderName		# Thanks to https://stackoverflow.com/a/11905011
	prevFolderName = folderName
	return prevFolderName

#### TODO:  ADD ERROR CHECKING and Exception Handling!  
rb = RoboBrowser(history=True,parser='html.parser')
def fetch_hidden_download_link(url): 
	# Group our downloaded files into a common folder (based on their URL)
	folderName = get_foldername_from_url(url)
	if folderName != prevFolderName:
		if prevFolderName != " ":
			print("\n=== '{}' is a NEW folderName ===".format(folderName)) 
		update_prevFolderName(folderName)

	download_path = os.getcwd() +os.sep+ 'VERIFY_Downloads' +os.sep + folderName +os.sep
	os.makedirs(download_path, exist_ok=True)

	print(url)	# It's always useful to know the original URL
	rb.open(url)
	
	# Get the hidden form
	hidden_form = rb.get_forms()[1]
	_debug_print(hidden_form)

	res = rb.submit_form(hidden_form)
	_debug_print( str(rb.parsed) )
		
	#  Thanks to: http://www.compjour.org/warmups/govt-text-releases/intro-to-bs4-lxml-parsing-wh-press-briefings/
	download_form = rb.find_all("form")[1]	# the second form will have our download link
	download_url = download_form.attrs['action']
	print(download_url)  #  The url is expected to look this: http://software.oldversion.com/download.php?f=YTo1OntzOjQ...

	'''  Get the *real* filename of the download from the Content-Disposition HTTP header
		 Thanks to: https://stackoverflow.com/a/37060758
	'''
	r = requests.get(download_url, allow_redirects=True)
	filename = rfc6266.parse_requests_response(r).filename_unsafe	
	print(filename)

	destFile_path = download_path + filename
	_debug_print(destFile_path)
	''' wget insisted on getting the filename from the HTTP headers, i.e.
		wget.download(download_url, destFile_path)  # fails with IndexError: list index out of range

		The SmartDL module on the hand... just works :)
	'''
	smart_dl = SmartDL(download_url, destFile_path, progress_bar=False)
	smart_dl.start()
	print('SUCCESS' if smart_dl.isSuccessful() else 'FAILED')

def main():	
	#  Note: you can scrape the URLs from oldversion.com
	#  with a wonderful & intuitive(!) tool like ParseHub :)
	#  Use this little trick to get (for example) a listing of all the Windows Utilities in a single page...
	#
	#  http://www.oldversion.com/windows/software/utilities/?section=&limit=1000&api=1
	#
	with open('urls.txt', 'r') as urls:
		for url in urls:
			### The hidden links should be downloadwd ASAP as they become expired within minutes...!
			fetch_hidden_download_link( url.strip() )

if __name__ == "__main__":
	main()
