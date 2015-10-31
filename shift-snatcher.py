import mechanize
import cookielib
import getpass
import re
import smtplib
from BeautifulSoup import BeautifulSoup
from os import path

#Format email (global)
emsg = "\r\n".join([
	"From: @gmail.com",
	"To: @gmail.com",
	"Subject: Open shifts",
	"",
	"BEST SHIFTS",
	"----------------------"])

def shiftPageParser(url):
	global emsg
	os = br.open(url).read()
	soup = BeautifulSoup(os)
	
	#Check if there are any posted shifts
	schedule = soup.findAll('div', attrs={'class':'schedule'})	
	if schedule[0].text.find("Posted by") != -1:
		dates = soup.findAll('tr')
		datesList = re.split(r"([A-Z][a-z]{2}[a,][a ][A-Z][a-z]{2}[a ][0-9]{1,2})",dates[0].text)
		datesList = [datesList[1],datesList[3],datesList[5],datesList[7],datesList[9],datesList[11],datesList[13]]
		#print datesList
		dateIndex = -1
		dateStr = ''
		timeStr = ''
		consStr = ''
		
		columns = soup.findAll('td')
		for col in columns:
			#Set new date if needed
			if col.has_key('class'):
				dateIndex = dateIndex + 1
				dateStr = datesList[dateIndex]
			#Check if there is an open shift in col			
			info = re.split(r"([0-9]{1,2}[a:][0-9]{1,2}[A-Z]{1,2}[a |a-]{3}[0-9]{1,2}[a:][0-9]{1,2}[A-Z]{1,2})",col.text)
			for str in info:
				if re.search(r"([0-9]{1,2}[a:][0-9]{1,2}[A-Z]{1,2}[a |a-]{3}[0-9]{1,2}[a:][0-9]{1,2}[A-Z]{1,2})", str) is not None: 
					timeStr = str
				if str.find("Posted by") != -1:
					consStr = str
					msg = dateStr + ' ' + timeStr + ' ' + consStr
					print msg
					emsg = "\r\n".join([emsg,
										msg])
					
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

br.form = list(br.forms())[0]

#username = raw_input('Enter username: ')
#password = getpass.getpass('Enter password: ')

br["username"] = ''#username #the key "username" is the variable that takes the username/email value   
br["password"] = '' #password    #the key "password" is the variable that takes the password value   

logged_in = br.submit()   #submitting the login credentials   

#Email stuff
fromaddr = '@gmail.com'
toaddrs = ['@gmail.com']

eusername = '' #raw_input('Enter gmail username: ')
epassword = '' #getpass.getpass('Enter gmail password: ')

#Print all open shifts (BEST,LSM,ARC)
bestURLList = ["https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-10-31","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-11-07","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-11-14","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-11-21","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-11-28","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/22/?start_date=2015-12-05"]
arcURLList  = ["https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-10-31","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-11-07","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-11-14","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-11-21","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-11-28","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/19/?start_date=2015-12-05"]
lsmURLList  = ["https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-10-31","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-11-07","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-11-14","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-11-21","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-11-28","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/24/?start_date=2015-12-05"]
dispURLList = ["https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/20/?start_date=2015-10-31","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/20/?start_date=2015-11-07","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/20/?start_date=2015-11-14","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/20/?start_date=2015-11-21","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/20/?start_date=2015-11-28","https://sc-apps-new.rutgers.edu/portal/scheduling/open_shifts/20/?start_date=2015-12-05"]

print 'Open Shifts'
print '-----------'
print ''
print 'BEST SHIFTS'
print '-----------'
print ''

	
for curr_url in bestURLList:
	shiftPageParser(curr_url)
			
print ''		
print 'ARC SHIFTS'
print '----------'
print ''

emsg = "\r\n".join([
	emsg,
	"ARC SHIFTS",
	"----------------------"])
	
for curr_url in arcURLList:
	shiftPageParser(curr_url)
	
print ''
print 'LSM SHIFTS'
print '----------'
print ''

emsg = "\r\n".join([
	emsg,
	"LSM SHIFTS",
	"----------------------"])
	
for curr_url in lsmURLList:
	shiftPageParser(curr_url)
	
print ''
print 'DISP SHIFTS'
print '-----------'
print ''

emsg = "\r\n".join([
	emsg,
	"DISP SHIFTS",
	"----------------------"])
	
for curr_url in dispURLList:
	shiftPageParser(curr_url)
	
file_path = "C:\Users\Admin\Desktop\shift.txt" //shift.txt
target = open(file_path, 'r+')
old_emsg = target.read()
target.seek(0)


#print old_emsg

#Send Email
if old_emsg != emsg:
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(eusername,epassword)
	for toaddr in toaddrs:
		server.sendmail(fromaddr,toaddr, emsg)
	server.quit()
	target.truncate()
	target.write(emsg)
target.close()
