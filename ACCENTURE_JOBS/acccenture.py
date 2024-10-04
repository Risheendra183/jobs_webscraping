import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Base URL for the job listings
base_url = "https://www.accenture.com/in-en/careers/jobsearch?jk=&sb=1&vw=0&is_rj=0&pg="

# Filenames for job data and links
json_filename = 'all_jobs_data6.json'
links_filename = 'job_links6.json'
progress_filename = 'last_page.txt'

# Function to save job data to the JSON file incrementally
def save_job_data_to_json(job_data):
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = []

    existing_data.append(job_data)

    with open(json_filename, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

# Function to save job links to a file dynamically
def save_job_links_to_json(job_links):
    if os.path.exists(links_filename):
        with open(links_filename, 'r') as json_file:
            existing_links = json.load(json_file)
    else:
        existing_links = []

    existing_links.extend(job_links)

    with open(links_filename, 'w') as json_file:
        json.dump(existing_links, json_file, indent=4)

# Function to save the last successfully scraped page number
def save_progress(page_number):
    with open(progress_filename, 'w') as f:
        f.write(str(page_number))

# Function to load the last successfully scraped page number
def load_progress():
    if os.path.exists(progress_filename):
        with open(progress_filename, 'r') as f:
            return int(f.read())
    return 0  # If no progress file exists, start from page 1

# Function to get job detail URLs from the search result pages
def get_job_links(page_number):
    job_links = []
    url = base_url + str(page_number)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.cmp-teaser__content__details-section"))
        )
        
        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.cmp-teaser__content__details-section")
        for card in job_cards:
            try:
                job_id = card.find_element(By.CSS_SELECTOR, "div.cmp-teaser__save-job-card").get_attribute("data-job-id")
                job_url = f"https://www.accenture.com/in-en/careers/jobdetails?id={job_id}"
                job_links.append(job_url)
            except (NoSuchElementException, StaleElementReferenceException):
                continue
    except (NoSuchElementException, TimeoutException):
        print(f"Error on page {page_number}: Could not find job elements")
    
    return job_links

# Function to scrape job details from each job URL
def scrape_job_details(job_url):
    driver.get(job_url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.cmp-title__text"))
        )
        job_data = {}

        job_data['JOB TITLE'] = driver.find_element(By.CSS_SELECTOR, "h1.cmp-title__text").text.strip()

        labels = driver.find_elements(By.CSS_SELECTOR, ".cmp-job-listing-hero__labels-container .cmp-text__label-small")
        job_data['LOCATION'] = labels[0].text.strip() if len(labels) > 0 else None
        job_data['JOB ID'] = labels[1].text.strip() if len(labels) > 1 else None
        job_data['JOB TYPE'] = labels[2].text.strip() if len(labels) > 2 else None

        description_content = driver.find_element(By.CLASS_NAME, "description-content").get_attribute("innerHTML")
        
        if "Project Role Description :" in description_content:
            job_description = description_content.split("Project Role Description :")[1].split("<br>")[0].strip()
            job_data['JOB DESCRIPTION'] = job_description.replace('</b>', '').strip()
        else:
            job_data['JOB DESCRIPTION'] = None

        if "Must have skills :" in description_content:
            skills_required = description_content.split("Must have skills :")[1].split("<br>")[0].strip()
            job_data['SKILLS REQUIRED'] = skills_required.replace('</b>', '').strip()
        else:
            job_data['SKILLS REQUIRED'] = None

        if "Minimum" in description_content:
            experience = description_content.split("Minimum")[1].split("year(s)")[0].strip()
            experience = experience.replace('</b>', '').strip()
            job_data['YEARS OF EXPERIENCE'] = f"{experience} years"
        else:
            job_data['YEARS OF EXPERIENCE'] = None

        if "Educational Qualification :" in description_content:
            educational_qualification = description_content.split("Educational Qualification :")[1].split("<br>")[0].strip()
            job_data['EDUCATIONAL QUALIFICATION'] = educational_qualification.replace('</b>', '').strip()
        else:
            job_data['EDUCATIONAL QUALIFICATION'] = None
        
        apply_link = driver.find_element(By.XPATH, "//a[contains(@class, 'cmp-button apply-job')]").get_attribute("href")
        job_data['APPLY LINK'] = apply_link

        return job_data
    except NoSuchElementException:
        return {
            'JOB TITLE': None,
            'LOCATION': None,
            'JOB ID': None,
            'JOB TYPE': None,
            'JOB DESCRIPTION': None,
            'SKILLS REQUIRED': None,
            'YEARS OF EXPERIENCE': None,
            'EDUCATIONAL QUALIFICATION': None,
            'APPLY LINK': None
        }

# Main program to extract job details
def main():
    # Load the last page number from the progress file
    start_page = load_progress()
    
    for page_number in range(start_page + 1, 5555):  # Start from the last saved page
        print(f"Scraping page {page_number}...")

        job_links = get_job_links(page_number)
        save_job_links_to_json(job_links)
        print(f"Saved {len(job_links)} job links from page {page_number}.")

        job_data_list = []
        for job_link in job_links:
            job_data = scrape_job_details(job_link)
            job_data_list.append(job_data)
            print(f"Job data scraped for {job_link}")

        # Save job data in bulk
        for job_data in job_data_list:
            save_job_data_to_json(job_data)

        # Save progress after completing each page
        save_progress(page_number)

    print("All job data scraped and saved.")

# Run the main program
try:
    main()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
