import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import re
import os

# Base URL for apply links
APPLY_BASE_URL = "https://career5.successfactors.eu/careers?company=SAP"

# Function to fetch and parse a single page
async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

# Function to extract job details from a single page
async def extract_job_details(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch_page(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract job links from the page
        job_links = [a['href'] for a in soup.select('a.jobTitle-link')]

        # Extract job details from each job link
        jobs = []
        for link in job_links:
            job_url = f"https://jobs.sap.com{link}"
            job_html = await fetch_page(session, job_url)
            job_soup = BeautifulSoup(job_html, 'html.parser')
            
            # Extract job details
            try:
                job_title = job_soup.find("span", {"data-careersite-propertyid": "title"}).get_text(strip=True)
                job_title = re.sub(r'\s*Job Details.*$', '', job_title).strip()
            except AttributeError:
                job_title = "Not Provided"

            company = "SAP"
            try:
                eligibility_criteria = job_soup.find("span", {"data-careersite-propertyid": "customfield3"}).get_text(strip=True)
            except AttributeError:
                eligibility_criteria = "Not Provided"

            try:
                location = job_soup.find("span", {"data-careersite-propertyid": "location"}).get_text(strip=True)
            except AttributeError:
                location = "Not Provided"

            try:
                job_type = job_soup.find("span", {"data-careersite-propertyid": "shifttype"}).get_text(strip=True)
            except AttributeError:
                job_type = "Not Provided"

            # Extract posted date
            try:
                posted_date = job_soup.find("span", {"data-careersite-propertyid": "date"}).get_text(strip=True)
            except AttributeError:
                posted_date = "Not Provided"

            # Extract years of experience using refined regex
            job_description = job_soup.find("div", {"class": "jobdescription"}).get_text(strip=True) if job_soup.find("div", {"class": "jobdescription"}) else "Not Provided"
            exp_matches = re.findall(r'(\d+)\s*[-–—]\s*(\d+)\s*years?|(\d+)\s*years?', job_description.lower())

            if exp_matches:
                years_of_exp = ', '.join([f"{m[0]}-{m[1]}" if m[1] else m[2] for m in exp_matches])
            else:
                years_of_exp = "Not Mentioned"

            # Apply link (base URL)
            apply_link = APPLY_BASE_URL

            job_data = {
                "company": company,
                "job_title": job_title,
                "eligibility_criteria": eligibility_criteria,
                "years_of_exp": years_of_exp,
                "location": location,
                "job_type": job_type,
                "posted_date": posted_date,
                "apply_link": apply_link  # Include apply link
            }
            # Avoid duplicate entries
            if job_data not in jobs:
                jobs.append(job_data)
        
        return jobs

# Function to get job details from multiple pages
async def main():
    base_url = "https://jobs.sap.com/search/?q=&sortColumn=referencedate&sortDirection=desc&optionsFacetsDD_customfield3=Graduate&startrow={}&scrollToTable=true"
    pages = [base_url.format(i * 25) for i in range(25)]  # Adjust number of pages as needed

    tasks = [extract_job_details(page) for page in pages]
    all_jobs = await asyncio.gather(*tasks)

    # Flatten the list of lists
    all_jobs = [job for sublist in all_jobs for job in sublist]

    # Save to JSON file
    os.makedirs('json', exist_ok=True)
    with open('json/sap_data.json', 'w') as file:
        json.dump(all_jobs, file, indent=4)

# Run the asynchronous tasks
asyncio.run(main())
