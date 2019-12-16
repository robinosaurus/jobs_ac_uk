import requests
from bs4 import BeautifulSoup
import csv
base_url = "https://www.jobs.ac.uk"

def set_params():
	print("Edit python file to change search terms. \nSetting other search parameters: ")
	params = {
		"search_date": input("Enter dates (with ',' to seperate, e.g. '1,2,3'): "),
		"search_month": input("Search month(s) (e.g. 'Nov,Dec'): "), #yes this will find things 1 month old - better than missing them
		"min_salary": int(input("Min salary: ")),
		"search_terms": [
			"clinical+trials",
			"programme+manager",
			"research+manager",
			"artificial+intelligence"]}
	params["search_date"] = params["search_date"].split(",")
	params["search_month"] = params["search_month"].split(",")

	return params

def num_results(search_terms):
	results = []
	for term in search_terms:
		r = requests.get(base_url+"/search/?keywords="+term)
		if r.status_code == 200:
			r_html = r.content
			r_soup = BeautifulSoup(r_html, "html.parser")
			r_obj = r_soup.find("strong")
			results.append({"term": term, "num_results": r_obj.text})
	return results #dict of term:num_results k:v pairs

def get_results(num_results):
	jobs_list = []
	for item in num_results:
		url = f"{base_url}/search/?keywords={item['term']}&pageSize={item['num_results']}&startIndex=0"
		r = requests.get(url)
		if r.status_code == 200:
			r_soup = BeautifulSoup(r.content, "html.parser")
			jobs = r_soup.find_all(class_="j-search-result__text")
			jobs_list += jobs
	print(len(jobs_list))
	print("jobs found")
	return jobs_list #list of all job objects for all terms, no other details

def compare_details(jobs_list, params):
	jobs_dict = []
	url_list = []
	for job in jobs_list:
		url = job.find("a")["href"]
		s = job.find(class_="j-search-result__info").get_text()
		s = s.split("£") #first in list is anything before first £, so ignore
		min_salary = ""
		if len(s) > 1:
			for c in s[1]:
				try:
					if isinstance(int(c),int) and len(min_salary) < 6: #because some include pennies or other numbers, and I'm not looking for jobs >£100k
						min_salary += c
				except:
					pass
			min_salary = int(min_salary)
		else:
			min_salary = 0
		e = job.find(class_="j-search-result__employer")
		employer = e.text.strip("\n")
		if min_salary >= params["min_salary"]:
			if url not in url_list:
				jobs_dict.append({
					"min_salary": min_salary,
					"url": f"{base_url}{url}",
					"employer": employer})
				url_list.append(url)
	return jobs_dict

def compare_dates(jobs_dict, params):
	error_list = []
	fieldnames = ["url", "min_salary", "employer"]
	with open("matching_jobs.csv", "w", newline='') as file:
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
	for job in jobs_dict:
		j = requests.get(job["url"])
		try:
			if j.status_code == 200:
				j_html = j.content
				j_soup = BeautifulSoup(j_html, "html.parser")
				d = j_soup.find(class_="j-advert-details__second-col")
				date = d.find("td")
				date = date.text
				day,month,year = date.split()
				try:
					int(day[1])
					date = day[0:2]
				except:
					date = day[0]
				month = month[0:3]
		except:
			print(f"error with date: {job['url']}")
			error_list.append(job['url'])

		if date in params["search_date"] and month in params["search_month"]:
			print(f"Job found: {job['employer']}")
			with open("matching_jobs.csv", "a", newline='') as file:
				writer = csv.DictWriter(file, fieldnames=fieldnames)
				writer.writerow(job)
		else:
			print(f"Old: {date} of {month}")
	with open("error_list.csv", "w") as file:
		writer = csv.writer(file)
		writer.writerow(error_list)

params = set_params()
nums = num_results(params["search_terms"])
all_jobs = get_results(nums)
jobs_list = compare_details(all_jobs, params)
compare_dates(jobs_list, params)
print("Done. \nCheck error list for pages with unreadable formatting")