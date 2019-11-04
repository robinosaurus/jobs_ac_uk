import requests
from bs4 import BeautifulSoup
from csv import writer

base_url = "https://www.jobs.ac.uk"
search_url = "/search/?keywords="
matching_jobs = []
dup_list = []

#default settings
params = {"url": base_url+search_url, 
	"search_day": [4], #posted [today, yesterday]
	"search_month": ["Nov"],
	"min_salary": 36000, #will exclude jobs where the starting salary is below this
	"max_salary": 100000, #not really useful (for me)
	"search_terms": [ #these probably create lots of duplicate results
		"clinical+trials"
		,"programme+manager"
		,"research+manager"
		]
	}

print(f"Current search for: {params['search_terms']}. For date: {params['search_day'][0]} {params['search_month'][0]}.")
change_params = input("Change params (y/n)?")
if change_params == "y":
	change_terms = input("Delete or append search terms (d/a)?")
	if change_terms == "d":
		params["search_terms"] = []
	new_terms = []
	while True:
		term = input("New search term (q to stop): ")
		term.replace(" ", "+")
		if term == "q":
			break
		else:
			params["search_terms"].append(term)

	params["search_day"] = [int(input("Search date (0-31):"))]
	params["search_month"] = [input("Search month (e.g. Jan, Feb):")]

for i in range(0,(len(params["search_terms"]))):
	results = requests.get(params["url"]+params["search_terms"][i])
	if results.status_code == 200:
		results_html = results.content
		results_soup = BeautifulSoup(results_html, "html.parser")

	result_object = results_soup.find("strong")
	num_results = int(result_object.text)
	size_url = f"&pageSize={num_results}&startIndex=0"

	results = requests.get(params["url"]+params["search_terms"][i]+size_url)
	if results.status_code == 200:
		search_term = params["search_terms"][i]
		print(f"get() success for search term: {search_term}")
		print(f"number of results: {num_results}")
		results_html = results.content
		results_soup = BeautifulSoup(results_html, "html.parser")

	jobs_list = results_soup.find_all(class_="j-search-result__text")
	jobs_dict = []
	for j in jobs_list:
		href = j.find("a")["href"]
		s = j.find(class_="j-search-result__info")
		text = s.get_text()
		text = text.split("£")
		min_salary = ""
		try:
			for c in text[1]:
				try:
					if isinstance(int(c), int):
						min_salary += c
				except:
					pass
		except:
			pass

		if len(min_salary) > 5:
			min_salary = 0
		elif min_salary == "":
			min_salary = 0
		else:
			min_salary = int(min_salary)
		
		max_salary = "0"
		try:
			for c in text[2]:
				try:
					if isinstance(int(c), int):
						max_salary += c
				except:
					pass
		except:
			pass
		max_salary = int(max_salary)

		if min_salary > params["min_salary"]:
			jobs_dict.append({"href": href, "min_salary": min_salary, "max_salary": max_salary})

	print(f"number of results in salary range: {len(jobs_dict)}")

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
				
				if date in params["search_day"] and month in params["search_month"]:
					match_url = f"{base_url}{url_end}"
					if match_url in dup_list:
						print("duplicate found")
					else:
						dup_list.append(match_url)
						employer_obj = job_soup.find(class_="j-advert__employer row-4") #employer
						employer = employer_obj.find("b")
						employer = employer.text.strip("\n")
						print(employer)
						matching_jobs.append([
							match_url, 
							job["min_salary"], 
							job["max_salary"],
							employer
						])
						print("new job found")
				else:
					print("old listing")
			except:
				pass
num_matches = len(matching_jobs)
print(f"Total new jobs found: {num_matches}")

filename = f"job_results_{params['search_day'][0]}_{params['search_month'][0]}.csv"

with open(filename, "w", newline='') as csv:
	writer = writer(csv)
	for job in matching_jobs:
		writer.writerow(job)