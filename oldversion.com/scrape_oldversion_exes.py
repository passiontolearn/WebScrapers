import rfc6266, requests  # for getting filename from content-disposition
import os
from pySmartDL import SmartDL
from robobrowser import RoboBrowser

DEBUG = False	# Set to True for debug print statements
def _debug_print(s):
    if DEBUG:
        print(s)

def get_hidden_download_link(url): 
	rb = RoboBrowser(history=True,parser='html.parser')
	rb.open(url)

	# Get the hidden form
	hidden_form = rb.get_forms()[1]
	_debug_print(hidden_form)

	res = rb.submit_form(hidden_form)
	_debug_print( str(rb.parsed) )

	### TODO:  ADD ERROR CHECKING and/or Exception Handling!  
		
	#  Thanks to: http://www.compjour.org/warmups/govt-text-releases/intro-to-bs4-lxml-parsing-wh-press-briefings/
	#
	download_form=rb.find_all("form")[1]	# the second form will have our download link
	download_url=download_form.attrs['action']
	print(download_url)
    #  The url is expected to look this: http://software.oldversion.com/download.php?f=YTo1OntzOjQ...
	
	'''  Get the *real* filename of the download from the Content-Disposition HTTP header
		 Thanks to: https://stackoverflow.com/a/37060758
	'''
	r = requests.get(download_url, allow_redirects=True)
	filename = rfc6266.parse_requests_response(r).filename_unsafe
	
	print(filename)
	destFile_path = os.getcwd() +os.sep+ 'Installers' +os.sep+ filename
	_debug_print(destFile_path)

	''' wget insisted on getting the filename from the HTTP headers, i.e.
		wget.download(download_url, destFile_path)  # fails with IndexError: list index out of range

		The SmartDL module on the hand... just works :)
	'''
	smart_dl = SmartDL(download_url, destFile_path, progress_bar=False)
	smart_dl.start()
	print('SUCCESS' if smart_dl.isSuccessful() else 'FAILED')

#  Note: you can scrape the URLs from oldversion.com
#  with a wonderful & intuitive(!) tool like ParseHub :)
#  Use this little trick to get (for example) a listing of all the Windows Utilities in a single page...
#
#  http://www.oldversion.com/windows/software/utilities/?section=&limit=1000&api=1
#
##### You should download the links ASAP - they will expire within minutes...!	
with open('urls.txt', 'r') as urls:
	for url in urls:
		get_hidden_download_link( url.strip() )
