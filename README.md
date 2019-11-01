# jobs_ac_uk
Custom search and url getter for jobs.ac.uk (python)

Useful if (like me) you find the default search on jobs.ac.uk total trash. 

On top of default search this adds:
  1) ability to filter out low grade jobs with a high upper salary that make up the majority of results for me.
    e.g. adding a minimum salary of 36000 will filter out all grade 7 jobs (ranging from £30-40k), which the default filter can't do
  2) filter by jobs added today. You can sort by date on the site, but without visiting every page it won't show when they were posted

Instructions:
  1) edit the params based on your criteria
  2) run to find new jobs posted
  3) results saved in csv in same folder, with mix/max salary, link, employer


Future versions might be able to:
  - edit params without opening up the .py
  - fix issues reporting min salary for jobs with no max salary
  - efficiency improvement (avoid re-searching links between terms, download all jobs and save to csv for lookup)
but don't hold your breath because current version works for me.
