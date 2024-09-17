import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

# Set up Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL to scrape
url = "https://tatatechnologies.ripplehire.com/candidate/?token=pUMIYomQw46RCgLl0Cyq&lang=en&source=CAREERSITE#list/bu=INDIA"

# Open the webpage
driver.get(url)
time.sleep(5)  # wait for the initial page load

# Scroll and load all job listings dynamically
job_links_set = set()  # Use a set to avoid duplicate job links
scroll_pause_time = 3
last_height = driver.execute_script("return document.body.scrollHeight")

# Scroll until no new jobs are loaded
while True:
    # Scroll down to the bottom
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(scroll_pause_time)  # wait for the new jobs to load
    
    # Get the job links after scrolling
    job_links = driver.find_elements(By.CSS_SELECTOR, 'a.job-title')
    for job_link in job_links:
        job_links_set.add(job_link.get_attribute('href'))  # Add job link to the set
    
    # Check if the scroll height has changed
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # Stop scrolling if no new content is loaded
    last_height = new_height

print(f"Total job links found: {len(job_links_set)}")

# Now that all job links are collected, we can proceed to scrape each job
job_data = []

# Iterate over each unique job link and scrape the data
for job_link in job_links_set:
    driver.get(job_link)
    time.sleep(2)  # wait for the page to load

    # Parse the job details page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        # Extract Job Title
        job_title = soup.find('h2').get_text(strip=True)

        # Extract Years of Experience
        experience = soup.find('i', class_='icon-glyph-111').find_parent('li').get_text(strip=True)

        # Extract Openings
        openings = soup.find('i', class_='icon-glyph-83').find_parent('li').get_text(strip=True)

        # Extract Location
        location = soup.find('li', class_='location-text').get_text(strip=True)

        # Extract Apply Link (use the current URL as the apply link)
        apply_link = job_link

        # Add company name
        company_name = "Tata Technologies"

        # Store the job data with company name first
        job_data.append({
            'Company': company_name,
            'Job Title': job_title,
            'Years of Experience': experience,
            'Openings': openings,
            'Location': location,
            'Apply Link': apply_link
        })

        print(f"Scraped: {job_title}")

    except Exception as e:
        print(f"Error scraping job: {job_link}, Error: {e}")

# Save job data to JSON file
with open('job_data.json', 'w') as json_file:
    json.dump(job_data, json_file, indent=4)

# Close the browser
driver.quit()

print("Job data has been scraped and saved to job_data.json")
