import mechanize
import cookielib
import getpass
from BeautifulSoup import BeautifulSoup

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

r = br.open('https://sc-apps-new.rutgers.edu/portal/auth/login/')

soup = BeautifulSoup(br.response().read())
pretty = soup.prettify()
pretty_utf8 = pretty.encode('utf-8')
r.set_data(pretty_utf8)
br.set_response(r)

#for form in br.forms():
#    print form.name   

#br.select_form(nr=1) #accessing form by their index. Since we have only one form in this example, nr =0. 
#br.select_form(name = "form name") Alternatively you may use this instead of the above line if your form has name attribute available.   

br.form = list(br.forms())[0]

username = raw_input('Enter username: ')
password = getpass.getpass('Enter password: ')

br["username"] = username #the key "username" is the variable that takes the username/email value   
br["password"] = password    #the key "password" is the variable that takes the password value   

logged_in = br.submit()   #submitting the login credentials   

#Print all open shifts (BEST,LSM,ARC)
bestURLList = {"https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-09-19","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-09-26","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-10-03","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-10-10","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-10-17","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-10-24","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-10-31","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-11-07","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-11-14","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-11-21","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-11-28","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-12-05"}
arcURLList = {"https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-09-19","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-09-26","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-10-03","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-10-10","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-10-17","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-10-24","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-10-31","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-11-07","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-11-14","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-11-21","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-11-28","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-12-05"}
lsmURLList = {"https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-09-19","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-09-26","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-10-03","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-10-10","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-10-17","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-10-24","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-10-31","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-11-07","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-11-14","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-11-21","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-11-28","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-12-05"}
print 'Open Shifts'
print '-----------'
print ''
print 'BEST SHIFTS'
print '-----------'
print ''
for curr_url in bestURLList:
	#print "Searching: " + curr_url
	os = br.open(curr_url).read()
	soup = BeautifulSoup(os)
	list = soup.findAll('div', attrs={'class':'schedule'})
	for p in list:
		print p.text

print ''		
print 'ARC SHIFTS'
print '----------'
print ''
for curr_url in arcURLList:
	#print "Searching: " + curr_url
	os = br.open(curr_url).read()
	soup = BeautifulSoup(os)
	list = soup.findAll('div', attrs={'class':'schedule'})
	for p in list:
		print p.text

print ''
print 'LSM SHIFTS'
print '----------'
print ''
for curr_url in lsmURLList:
	#print "Searching: " + curr_url
	os = br.open(curr_url).read()
	soup = BeautifulSoup(os)
	list = soup.findAll('div', attrs={'class':'schedule'})
	for p in list:
		print p.text
	
'''
os = br.open("https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-09-19").read()
soup = BeautifulSoup(os)
list = soup.findAll('div', attrs={'class':'scheduleShift '})
for p in list:
	print p.text
	#print p.find('p' , attrs={'class':'startTime'})
	#print p.find('div' , attrs ={'style':'width: 100%; text-align: center;'})
'''
#print(os) #printing the body of the redirected url after login  

#req = br.open("http://school.dwit.edu.np/mod/assign/").read() 
#accessing other url(s) after login is done this way

