import requests
from bs4 import BeautifulSoup
import json
import re
from concurrent.futures import ThreadPoolExecutor

# Base URL for job listings
base_url = 'https://stripe.com/jobs/search?skip='

# Function to extract job details from a single job detail page
def extract_job_details(job_page_soup, job_url):
    job_details = {}
    
    # Add company field at the top
    job_details['company'] = 'STRIPE'

    # Extract Job Title
    title_tag = job_page_soup.find('h1', class_='Copy__title')
    job_details['Job Title'] = title_tag.text.strip() if title_tag else None

    # Extract office locations
    office_tag = job_page_soup.find('p', string='Office locations')
    job_details['office_locations'] = office_tag.find_next_sibling('p').text.strip() if office_tag else None

    # Extract job type
    job_type_tag = job_page_soup.find('p', string='Job type')
    job_details['job_type'] = job_type_tag.find_next_sibling('p').text.strip() if job_type_tag else None

    # Extract Team
    team_tag = job_page_soup.find('p', string='Team')
    job_details['team'] = team_tag.find_next_sibling('p').text.strip() if team_tag else None

    # Extract job description
    description_tag = job_page_soup.find('div', class_='JobDetailCard__description')
    description_text = description_tag.get_text() if description_tag else ''

    # Extract years of experience using regex
    experience_match = re.search(r'(\d+)\+?\s+years', description_text)
    job_details['years_of_experience'] = experience_match.group(1) + '+ years' if experience_match else None

    # Construct the apply link dynamically
    job_details['apply_link'] = job_url + '/apply'

    return job_details

# Function to scrape job detail page
def scrape_job_details(job_url):
    response = requests.get(job_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return extract_job_details(soup, job_url)

# Function to scrape job listings from the main page
def scrape_job_listings(page_number):
    url = base_url + str(page_number * 100)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_links = []

    # Find all job listing links
    job_listings = soup.find_all('a', class_='Link JobsListings__link')
    for job_listing in job_listings:
        job_page_url = 'https://stripe.com' + job_listing['href']
        job_links.append(job_page_url)

    return job_links

# Function to scrape job details in parallel
def scrape_all_job_details(job_links):
    job_data = []
    with ThreadPoolExecutor() as executor:
        job_data = list(executor.map(scrape_job_details, job_links))
    return job_data

# Main function to scrape all pages
def scrape_all_pages(num_pages):
    all_job_links = []
    for i in range(num_pages):
        print(f"Scraping page {i + 1}...")
        job_links = scrape_job_listings(i)
        all_job_links.extend(job_links)

    # Scrape job details in parallel
    print("Scraping job details...")
    all_jobs = scrape_all_job_details(all_job_links)
    
    # Save job data to JSON file
    with open('stripe_jobs.json', 'w') as f:
        json.dump(all_jobs, f, indent=4)
    
    print(f"Job data has been saved to stripe_jobs.json")

# Scrape the first 8 pages
if __name__ == '__main__':
    scrape_all_pages(8)
