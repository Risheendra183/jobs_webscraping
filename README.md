Job Data Scraper
This project is a Python-based web scraper that extracts job details from SAP's job listing site. It fetches job postings from multiple pages, extracts relevant job information, and saves the results in a JSON file.

Features
Asynchronously fetch job data from multiple pages.
Extract details including job title, company, eligibility criteria, location, job type, and posted date.
Handle various formats of experience requirements.
Avoid duplicate entries based on job title, location, and posted date.
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/job-data-scraper.git
cd job-data-scraper
Install Dependencies:

This project requires Python 3.7+ and the following Python packages:

aiohttp: For asynchronous HTTP requests.
beautifulsoup4: For parsing HTML.
json: For handling JSON data.
re: For regular expressions.
You can install the dependencies using pip:

bash
Copy code
pip install aiohttp beautifulsoup4
Usage
Run the Scraper:

To start the scraper and save the job data to a JSON file, execute the following command:

bash
Copy code
python scraper.py
This will generate a json/job_data.json file with the extracted job details.

Inspect the Output:

The output JSON file (json/job_data.json) will contain an array of job postings, each with the following fields:

company: The company offering the job (e.g., "SAP").
job_title: The title of the job position.
eligibility_criteria: The required qualifications for the job.
years_of_exp: The experience required for the job.
location: The location of the job.
job_type: The type of employment (e.g., "Regular Full Time").
posted_date: The date the job was posted.
