import csv
import re
import os
from bs4 import BeautifulSoup
import time
from selenium import webdriver


niche_links = ["https://www.niche.com/colleges/harvard-university/majors/",
"https://www.niche.com/colleges/princeton-university/majors/",
"https://www.niche.com/colleges/yale-university/majors/",
"https://www.niche.com/colleges/dartmouth-college/majors",
"https://www.niche.com/colleges/columbia-university/majors",
"https://www.niche.com/colleges/university-of-pennsylvania/majors",
"https://www.niche.com/colleges/brown-university/majors",
"https://www.niche.com/colleges/cornell-university/majors/",
"https://www.niche.com/colleges/massachusetts-institute-of-technology/majors",
"https://www.niche.com/colleges/california-institute-of-technology/majors",
"https://www.niche.com/colleges/stanford-university/majors/",
"https://www.niche.com/colleges/university-of-chicago/majors/",
"https://www.niche.com/colleges/duke-university/majors/",
"https://www.niche.com/colleges/johns-hopkins-university/majors/",
"https://www.niche.com/colleges/northwestern-university/majors/",
"https://www.niche.com/colleges/rice-university/majors/",
"https://www.niche.com/colleges/vanderbilt-university/majors/",
]

browser = webdriver.Chrome('/Users/yji/Documents/chromedriver')

f = open("all_majors.txt","w+")

for hyp in niche_links:
	uni = ""
	match = re.search(r'https://www.niche.com/colleges/(.*)/majors',hyp)
	if match:
		uni = match.group(1)
	browser.get(hyp)
	html_doc = browser.execute_script("return document.body.innerHTML")
	soup0 = BeautifulSoup(html_doc, 'html.parser')

	majors = []
	find_majors = soup0.find_all(class_="major-ranking__title")
	if find_majors:
		for i in find_majors:
			str1 = i.get_text()
			match = re.search(r"Best Colleges for (.*) in America",str1)
			if match:
				majors.append(match.group(1))
			else:
				majors.append(str1)

	popular = []
	find_popular = soup0.find_all(class_="popular-entity__name")
	if find_popular:
		for i in find_popular:
			popular.append(i.get_text())

	f.write(uni + ": " + '\n')
	f.write("Top Ranked Majors:\n")
	for m in majors:
		f.write(m + '\n')
	f.write("\nMost Popular Majors:\n")
	for p in popular:
		f.write(p + '\n')
	f.write('\n\n')


