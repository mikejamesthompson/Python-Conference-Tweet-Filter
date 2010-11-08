import sys, urllib, re
from BeautifulSoup import BeautifulSoup

def getHTML(url):
	sock = urllib.urlopen(url)
	html = sock.read()
	sock.close()
	return html

def getTweets(url):
	"""Get HTML, extract tweets, strip html tags, process content and write to a file"""
	html = getHTML(url)
	soup = BeautifulSoup(html)
	tables = soup.find(re.compile('^table'), {'id':'transcript'})
	rows = tables.findAll(re.compile('^tr'))
	output = open('output/output.txt', 'a')
	
	for row in rows:
		try:
			#Find third cell in row (if not present throws IndexError) and output formatted HTML
			cell = row.findAll(re.compile('^td'))[2]
			tweet = cell.prettify() 
			
			# Strip html and excess whitespace
			tweet = re.sub('<\w*?[^>]*>','',tweet)
			tweet = re.sub('<\/\w*?[^>]*>','',tweet)
			tweet = re.sub('\s+',' ',tweet)
			
			# Remove @s
			tweet = re.sub('\@\s{1}[^\s]+','',tweet)
			
			# Remove keywords
			tweet = re.sub(r'(?i)(e20s|summit|rt|Frankfurt)\b','', tweet)
			tweet = re.sub(r'(?i)(e20|e2\.0|enterprise 2\.0)\b','', tweet)
			
			# Two-word substitutions
			tweet = re.sub(r'(?i)change management', 'Change~management', tweet)
			tweet = re.sub(r'(?i)social business', 'Social~business', tweet)
			
			output.write(tweet + "\n")
			
		except IndexError:
			pass
			
	output.close()
	

if __name__ == "__main__":
	getTweets("http://wthashtag.com/transcript.php?page_id=6265&start_date=2010-10-27&end_date=2010-11-01&export_type=HTML")



