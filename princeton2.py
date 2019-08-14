import csv
import re
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen

c = csv.writer(open("Princeton_Programs.csv", "w"))
c.writerow(["Program","Name","Title1","Degree","Website","CV_Link","Photo_Link","Research_Interests","Title2","Title3","Email"])

#links = ["https://philosophy.princeton.edu/people/faculty","https://www.cs.princeton.edu/people/faculty","https://history.princeton.edu/people/faculty","http://www.ee.princeton.edu/people/faculty"]
links = []
for dirpath, dirnames, files in os.walk('/Users/yji/Desktop/Cheese/Princeton'):
  #print('Found directory: {dirpath}')
  for file_name in files:
    links.append('Princeton/' + file_name)

links.sort()

for hyp in links:
	program = ""
	match = re.search(r"Princeton/([a-zA-Z\s-]+)",hyp)
	print(hyp)
	if match:
		program = match.group(1)
		#print(program)
	#f = open(program+".txt","w+")
	html_doc = open(hyp,"rb")

	soup = BeautifulSoup(html_doc.read(), 'html.parser')

	find_people = soup.find_all(True,{"class":["views-row",re.compile(r'row-[0-9]+'),"people-grid-person-info",
		"people-2_col-wrapper","people-page-person-container","person"]})
	if find_people:
		for people in find_people:
			name = degree = ""
			email = web = cv = photo = interests = ""
			title = ["","",""]
			####################
			# Name aka title
			# Why is ORFE saying "lastname"?
			# english: "name"
			find_name = people.find(True,{"class":["views-field-title","views-field-field-lastname","name","people-grid-name-linked",
				"people-page-name","person-name"]})
			if find_name != None:
				name = find_name.get_text()
			else:
				find_name = people.find('h2')
				if find_name != None:
					name = find_name.get_text()
				else:
					find_name = people.find('h6')
					if find_name:
						name = find_name.get_text()


			####################
			##EE label: all in one, separated by <br>
			find_title = people.find(class_="views-field-field-faculty-title")
			if find_title != None:
				div = str(find_title.find('div'))
				match = re.search(r'<div class="field-content">([a-zA-Z0-9,.+\s\'-]+)<br/>([a-zA-Z0-9,.+\s\'-]+)<br/>([a-zA-Z0-9,.+\s\'-]+)</div>',str(div))
				if match:
					title[0] = match.group(1)
					title[1] = match.group(2)
					title[2] = match.group(3)
				else:
					match = re.search(r'<div class="field-content">([a-zA-Z0-9,.+\s\'-]+)<br/>+([a-zA-Z0-9,.+\s\'-]+)</div>',str(div))
					if match:
						title[0] = match.group(1)
						title[1] = match.group(2)
					else:
						match = re.search(r'<div class="field-content">([a-zA-Z0-9,.+\s\'-]+)</div>',str(div))
						if match:
							title[0] = match.group(1)
			else:
				#why another? they are associated faculty; where is my hair?
				find_title = people.find(class_="field-name-field-faculty-title")
				if find_title != None:
					match = find_title.find_all(class_="even")
					if match:
						n = 0 
						for i in match:
							title[n] = i.get_text()
							n += 2

					match = find_title.find_all(class_="odd")
					if match:
						n = 1
						for i in match:
							title[n] = i.get_text()
							n += 2
			##philosophy label: one title, one position
			#Psych: self-evident, very nice(great css!) and simple(only ONE title!) I love psych people!!	
			#English: "position"... elegante!!!
			if title[0] == "":
				find_title = people.find(True,{"class":["views-field-field-person-title","views-field-field-psych-title","views-field-field-title",
					"position","first","contact-data","person-title"]})
				if find_title:
					title[0]=find_title.get_text()
				# just for phi for now
				find_title = people.find(True,{"class":["views-field-field-person-position","last"]})
				if find_title:
					title[1]=find_title.get_text()
			find_degree = people.find(class_="person-degree")
			if find_degree:
				degree = find_degree.get_text()


			find_email = people.find(True,{"class":["views-field-field-email","field-name-field-email","views-field-field-person-email",
				"views-field-field-psych-email","views-field-mail","people-grid-email","email","people-page-email","person-address-item"]})
			if find_email:
				email = find_email.get_text()
				match = re.search(r'Email: (.*)',email)
				if match:
					email = match.group(1)
			#a bit diff for ENG
			find_email = people.find(True,{"class":["contact"]})
			if find_email and find_email.a:
				email = find_email.a.get_text()


			# Photo: very important for department full links!!

			find_photo = people.find(True,{"class":["views-field-field-person-photo","field-name-field-profile-picture","views-field-field-profile-picture","views-field-field-psych-faculty-photo",
				"views-field-picture","staff-photo","content","people-photo","people-page-image-container","person-photo"]})
			if find_photo and find_photo.img:
				photo = find_photo.img['src']
					

			full_web_link = ""
			find_web = people.find(class_="views-field-field-person-url")
			if find_web != None:
				web = find_web.get_text()
				match = re.search(r'Website: (.*)',web)
				if match:
					web = match.group(1)
			else:
				#go EE and Psych!!!
				match = re.search(r'(.*)edu',photo)
				if match:
					full_web_link = match.group(1) + "edu"
				else:
					full_web_link = "http://www.cs.princeton.edu"
					photo = full_web_link + photo

				find_web = people.find(True,{"class":["views-field-title","name","people-grid-name-linked","people-page-name","person-links"]})
				if find_web and find_web.a:
					href = find_web.a['href']
					match = re.search(r'(.*)edu',href)
					if match:
						web = href
					else:
						web = full_web_link + href
				else:
					find_web = people.find('h2')
					if find_web and find_web.a:
						web = full_web_link + find_web.a['href']
			#ORFE people here! Also very simple, maybe just for someone big
			if web == "":
				find_web = people.find(class_="views-field-field-lastname")
				if find_web and find_web.a:
					web = find_web.a['href']
			#ams
			if web == "":
				find_web = people.find('h6')
				if find_web and find_web.a:
					web = find_web.a['href']
			# I love CS FOREVER!
			web_cs = []
			#if web == "":
				
			find_web = people.find(class_="person-links")
			if find_web and find_web.find_all('a'):
				for i in find_web.find_all('a'):
					web_cs.append(i['href'])

			# only phi is nice so far, though it's just pdf
			find_cv = people.find(class_="views-field-field-person-cv")
			if find_cv and find_cv.a:
				cv = find_cv.a["href"]

			
			# only EE got this + ORFE
			find_interests = people.find(class_="views-field-field-application-areas")
			if find_interests:
				if find_interests.find_all('li') != None:
					for i in find_interests.find_all('li'):
						interests += i.get_text() + "; "
			else:
				find_interests = people.find(class_="views-field-field-researcharea")
				if find_interests:
					if find_interests.find_all('a') != None:
						for i in find_interests.find_all('a'):
							interests += i.get_text() + "; "
				else:
					find_interests = people.find(class_="person-research-interests")
					if find_interests:
						interests = find_interests.get_text()

			c.writerow([program,name,title[0],degree,web,cv,photo,interests,title[1],title[2],email])
			#f.write(people.get_text())

	#f.close()
	#if soup.find_allviews-field-field-person-title
