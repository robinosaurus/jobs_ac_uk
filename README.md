# jobs_ac_uk
Custom search and url getter for jobs.ac.uk (python)

Useful if (like me) you find the default search on jobs.ac.uk total trash. 

On top of default search this adds:
  1) ability to filter out low grade jobs with a high upper salary that make up the majority of results for me.
    e.g. adding a minimum salary of 36000 will filter out all grade 7 jobs (ranging from £30-40k), which the default filter can't do
  2) filter by jobs added today. You can sort by date by default, but without visiting every page it won't show which are new/old

Instructions:
  1) edit the params based on your criteria
  2) run to find new jobs posted today
  
Future versions might be able to:
  - save output with job title
  - edit params without opening up the .py
  - search multiple terms and remove duplicates
  - search over a range of dates
but don't hold your breath because current version works for me.
