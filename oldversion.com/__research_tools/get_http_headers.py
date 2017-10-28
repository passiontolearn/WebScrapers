import urllib.request

response = urllib.request.urlopen('http://software.oldversion.com/download.php?f=YTo1OntzOjQ6InRpbWUiO2k6MTUwOTEzNTM5OTtzOjI6ImlkIjtpOjIzMDg2O3M6NDoiZmlsZSI7czoyMToiZGFlbW9uLXRvb2xzLTItNzAubXNpIjtzOjM6InVybCI7czo1MToiaHR0cDovL3d3dy5vbGR2ZXJzaW9uLmNvbS93aW5kb3dzL2RhZW1vbi10b29scy0yLTcwIjtzOjQ6InBhc3MiO3M6MzI6IjcxYWNlYTE1ZmU3Y2Y5ZTA2MjlhY2Y0YWE1ZWIzZWE2Ijt9')
print ('RESPONSE:', response)
print ('URL     :', response.geturl())

headers = response.info()
print ('DATE    :', headers['date'])
print ('HEADERS :')
print ('---------')
print (headers)

#data = response.read()
#print 'LENGTH  :', len(data)
#print 'DATA    :'
#print '---------'
#print data
