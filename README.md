Job Scraper
Overview
This Python script asynchronously scrapes job postings from SAP's job portal. It extracts relevant job details such as job title, eligibility criteria, location, job type, posted date, and years of experience. The extracted data is saved into a JSON file.

Features
Asynchronously fetches and processes job listings from multiple pages.
Extracts job details including:
Job title
Eligibility criteria
Location
Job type
Posted date
Years of experience
Handles different formats of experience requirements, such as ranges and single years.
Saves the collected data into a JSON file.
Requirements
Python 3.7+
aiohttp library for asynchronous HTTP requests
BeautifulSoup library for HTML parsing
re module for regular expressions
Installation
Clone the repository or download the script.

Install the required libraries:

bash
Copy code
pip install aiohttp beautifulsoup4
Usage
Ensure the script is saved in a .py file (e.g., job_scraper.py).

Run the script:

bash
Copy code
python job_scraper.py
The script will scrape job postings from SAP's job portal, process the data, and save it to json/job_data.json.

Configuration
Number of pages: The script is configured to scrape 25 pages by default. You can adjust this by modifying the pages list in the main() function.

Job link processing: The script tracks processed job URLs and identifiers to avoid duplicates.

Example Output
The JSON file (json/job_data.json) will contain job entries in the following format:

json
Copy code
[
    {
        "company": "SAP",
        "job_title": "P2P Compliance Associate (Data Processing Enablement)",
        "eligibility_criteria": "Graduate",
        "years_of_exp": "2-3 years",
        "location": "Pasig City, PH, 1605",
        "job_type": "Regular Full Time",
        "posted_date": "Sep 8, 2024"
    },
    ...
]
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any questions or feedback, please reach out to your.email@example.com.
