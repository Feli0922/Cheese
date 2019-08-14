from bs4 import BeautifulSoup
from selenium import webdriver

links = ["https://web.astro.princeton.edu/people/astronomy-faculty"]

browser = webdriver.Chrome('/Users/yji/Documents/chromedriver')


for hyp in links:
	browser.get(hyp)
	html_doc = browser.execute_script("return document.body.innerHTML")
	soup0 = BeautifulSoup(html_doc, 'html.parser')
	for script in soup0(["script", "style"]):
		script.extract()    # rip it out
	
	# get text
	text = soup0.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)
	print(text)