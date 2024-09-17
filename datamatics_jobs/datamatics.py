import requests
from bs4 import BeautifulSoup
import json

# URL of the job openings page
url = 'https://www.datamatics.com/human-resources/job-openings'

# Send a GET request to fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all job posting cards
job_cards = soup.find_all('div', class_='accordion-item')

# Initialize a list to hold job information
jobs_data = []

# Loop through each job card and extract relevant information
for item in job_cards:
    try:
        # Extract job title and experience
        title_div = item.find('div', class_='accordion-title')
        title_text = title_div.text.strip() if title_div else None
        if title_text:
            job_title = title_text.split('|')[0].strip()
            exp_needed = title_text.split('|')[1].replace("EXP :", "").strip() if '|' in title_text else None
        else:
            job_title = exp_needed = None
        
        # Extract the table containing the job details
        table = item.find('table', class_='beta')
        if not table:
            raise Exception("Job table not found")

        rows = table.find_all('tr')

        # Look for the row with 'Job Location' and extract location
        location = None
        for row in rows:
            if row.find('td') and 'Job Location' in row.find('td').text:
                location = row.find_all('td')[1].text.strip()
                break

        # Extract job description and eligibility criteria
        job_description = None
        eligibility_criteria = None

        for row in rows:
            if row.find('td') and 'Job Desc' in row.find('td').text:
                job_desc_table = row.find_all('td')[1]
                job_desc_soup = BeautifulSoup(str(job_desc_table), 'html.parser')
                
                # Extract Key Responsibilities
                key_responsibilities_soup = job_desc_soup.find('strong', string=lambda text: text and 'Key Responsibilities' in text)
                if key_responsibilities_soup:
                    job_description = [li.text.strip() for li in key_responsibilities_soup.find_next('ul').find_all('li')]
                
                # Extract Competencies
                competencies_soup = job_desc_soup.find('strong', string=lambda text: text and 'Competencies' in text)
                if competencies_soup:
                    eligibility_criteria = [li.text.strip() for li in competencies_soup.find_next('ul').find_all('li')]
                else:
                    # Search for the term "Competencies" if not in strong tags
                    paragraphs = job_desc_soup.find_all('p')
                    for paragraph in paragraphs:
                        if 'Competencies' in paragraph.text or 'Desired Skills' in paragraph.text:
                            ul_tag = paragraph.find_next('ul')
                            if ul_tag:
                                eligibility_criteria = [li.text.strip() for li in ul_tag.find_all('li')]
                                break

        # Extract apply link from the last <tr> tag
        apply_link = rows[-1].find_all('td')[1].text.strip() if len(rows) > 0 and len(rows[-1].find_all('td')) > 1 else None

        # Extract company name from the website URL
        company = "Datamatics"

        # Append job details to the list
        jobs_data.append({
            "company": company,
            "location": location,
            "job_title": job_title,
            "exp_needed": exp_needed,
            "Eligibility_criteria": eligibility_criteria,
            "job_description": job_description,
            "apply_link": apply_link
        })
    except Exception as e:
        print(f"Error extracting job details: {e}")
        continue

# Write the JSON data to a file named datamatics.json
with open('datamatics.json', 'w') as json_file:
    json.dump(jobs_data, json_file, indent=4)

print("Data has been written to datamatics.json successfully.")
