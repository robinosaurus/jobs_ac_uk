import requests
from bs4 import BeautifulSoup
import datetime

base_url = "https://www.jobs.ac.uk"
search_url = "/search/?keywords="

#default settings
params = {"url": base_url+search_url, 
	"search_day": 31, #posted today
	"search_month": "Oct",
	"min_salary": 36000, #will exclude jobs where the starting salary is below this
	"max_salary": 100000, #not really useful (for me)
	"search_terms": [ #these probably create lots of duplicate results
		"programme+manager", 
		"clinical+trials", 
		"research+manager"
		]
	}

results = requests.get(params["url"]+params["search_terms"][0])
if results.status_code == 200:
	print("get() success")
	results_html = results.content
	results_soup = BeautifulSoup(results_html, "html.parser")

result_object = results_soup.find("strong")
num_results = int(result_object.text)
print(f"Number of results: {num_results}")
size_url = f"&pageSize={num_results}&startIndex=0"

results = requests.get(params["url"]+params["search_terms"][0]+size_url)
if results.status_code == 200:
	print("get() success")
	results_html = results.content
	results_soup = BeautifulSoup(results_html, "html.parser")

jobs_list = results_soup.find_all(class_="j-search-result__text")
jobs_dict = []
for j in jobs_list:
	href = j.find("a")["href"]
	s = j.find(class_="j-search-result__info")
	text = s.get_text()
	text = text.split("£")
	try:
		salary = ""
		for c in text[1]:
			try:
				if isinstance(int(c), int):
					salary += c
			except:
				pass
	except:
		salary = 0
	salary = int(salary)
	if salary > params["min_salary"]:
		jobs_dict.append({"href": href, "salary": salary})

print(f"Total jobs in salary range: {len(jobs_dict)}")

matching_jobs = []

for job in jobs_dict:
	url_end = job["href"]
	r = requests.get(f"{base_url}{url_end}")
	if r.status_code == 200:
		try:
			job_html = r.content
			job_soup = BeautifulSoup(job_html, "html.parser")
			date_object = job_soup.find(class_="j-advert-details__second-col")
			date = date_object.find("td")
			date = date.text
			day,month,year = date.split()
			date = day[0]
			try:
				if isinstance(int(day[1]), int):
					date += day[1]
			except:
					pass
			date = int(date)
			month = month[0:3]
			if date == params["search_day"] and month == params["search_month"]:
				match_url = f"{base_url}{url_end}"
				print(match_url)
				matching_jobs.append(match_url)
				print("new job found")
				#sleep(1)
			else:
				print("old")
		except:
			pass
print("List of today's urls:")
print(matching_jobs)
		#if date listed matches params
		#add to dict
		#wait(2)

#print(matching_jobs)