# Auto_Applier

## Purpose
The purpose of this project is to search by position and scrape the job links from Glassdoor's jobs page, and then automatically apply to those links. This will only apply to the positions that use common application pages like Lever. If a company uses their own personal jobs page, this won't successfully apply to those. The idea with this project is to lean on quantity to secure interviews, and to forego personalization steps like a cover letter. Ideally, this should be used in tandem with a more manual personalized approach for the higher value jobs

## Setup
1. Copy the `personal_info_template.py` and rename to `personal_info.py`
2. Fill out the information in `personal_info.py` with your info
3. Move a copy of your resume into the project folder
4. Make sure the name of your resume is changed in the `resume` field of `personal_info.py`
5. Open the `Glassdoor_Scraper.py` and change the position you are searching for.
6. Run `Glassdoor_Scraper.py`
7. Run `auto_applier.py`

## To Do
- Test the Lever Applier
- Add a check for if the job has already been applied to
- Add an update to the already applied list after a successful application
- Add a function to track jobs not applied to
- Add folders in project for organization, update pathing in code to reflect change
- Create a config file so all of the various details that the user can change are in one location
- Add additional appliers for greenhouse, myworkday, and taleo (greenhouse and lever cover about 40% of jobs, myworkday and taleo brings the number past 50%)
- Update GD Scraper to scrape multiple position titles

# Possible Further Development
- Scrape job links from more than Glassdoor
- Add more of the common application sites