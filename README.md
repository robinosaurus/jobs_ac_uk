# jobs_ac_uk
Custom search and url getter for jobs.ac.uk (python)

Useful if you also find the default search on jobs.ac.uk total trash.

On top of default search this adds:
  1) ability to filter out low grade jobs with a high upper salary that make up the majority of results for me.
    e.g. adding a minimum salary of 36000 will filter out all grade 7 jobs (ranging from £30-40k), which the default filter can't do
  2) filter by jobs added today. You can sort by date added on the site, but without visiting every page it won't show when they were  posted

Instructions:
  1) edit the search terms based on your criteria
  2) run to find new jobs posted
  3) results saved in csv in same folder, with mix/max salary, link, employer
  4) check jobs that look good, check error list for jobs where date couldn't be scraped

Fixed/added in V0.2:
  - multiple search terms at once
  - saves output as csv

Fixed/added in V0.3:
  - edit params without opening up the .py
  - fix issues reporting min salary for jobs with no max salary

Fixed in V1.0:
  - Now recognises errors (caused by extra bespoke formatting on paid ads) and adds to an error list
  - Tidied and shortened code
  - Search terms baked in, edit python file to change (this reflects how I used it - run once every few days with the same terms)
  
No more updates because I've found a job.
