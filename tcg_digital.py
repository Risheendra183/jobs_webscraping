import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage to scrape
url = "https://www.tcgdigital.com/careers/"

# Send a GET request to the URL
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize an empty list to store job data
job_data = []

# Find all job listings by locating the tab titles
tab_titles = soup.find_all('div', class_='elementor-tab-title')

for tab_title in tab_titles:
    # Get the job title
    job_title = tab_title.find('a', class_='elementor-toggle-title').text.strip()
    
    # Click on the tab to reveal job details (simulated by extracting details)
    # Note: This is a simplified approach; actual dynamic content may require more complex handling.
    tab_content = soup.find('div', {'id': tab_title['aria-controls']})
    
    if tab_content:
        # Initialize a dictionary to store job details, including the company name
        job_details = {
            "Company": "TCG DIGITAL",  # Add company name
            "Job Title": job_title
        }
        
        # Extract job details
        for row in tab_content.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) == 2:
                key = columns[0].get_text(strip=True).replace(':', '')
                value = columns[1].get_text(strip=True)
                
                # Store experience in a specific way if found
                if key == "Experience":
                    key = "Years of Experience"
                
                job_details[key] = value
        
        # Add job details to the job data list
        job_data.append(job_details)

# Save the job data to a JSON file
with open('job_data.json', 'w') as json_file:
    json.dump(job_data, json_file, indent=4)

print("Job data has been scraped and saved to 'job_data.json'.")
