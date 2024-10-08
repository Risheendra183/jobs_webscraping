# Job Scraper

This project is an asynchronous web scraper designed to extract job details from a careers website. The script fetches job postings, extracts relevant details, and saves them in a structured JSON format.

## Features

- **Asynchronous Scraping:** Efficiently fetches multiple job pages simultaneously using `aiohttp` and `asyncio`.
- **BeautifulSoup Integration:** Parses the HTML content of job pages to extract necessary details.
- **Years of Experience Extraction:** Extracts the number of years of experience required from job descriptions using regular expressions.
- **Duplicate Filtering:** Ensures that no duplicate job entries are saved in the final JSON file.
- **JSON Output:** Saves the scraped job data in a neatly formatted JSON file.

## Project Structure


## Prerequisites

- Python 3.7 or higher
- `aiohttp` for asynchronous HTTP requests
- `BeautifulSoup` for parsing HTML content
- `re` for regular expressions

You can install the required libraries using the following command:

```bash
pip install aiohttp beautifulsoup4

## How to Run the Project

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/job-scraper.git
    cd job-scraper
    ```

2. **Install the required dependencies:**

    ```bash
    pip install aiohttp beautifulsoup4
    ```

3. **Run the scraper:**

    ```bash
    python main.py
    ```

4. **View the output:**

   The scraped job data will be saved in the `json/job_data.json` file.

Job Data Structure
The output JSON file contains an array of job objects with the following structure:

json

[
    {
        "company": "  ",
        "job_title": "Job Title",
        "eligibility_criteria": " ",
        "years_of_exp": " ",
        "location": "Location",
        "job_type": "Job Type",
        "posted_date": " ",
        "apply_link": "https://jobs.sap.com/talentcommunity/apply/1102475701/?locale=en_US"
    }

Customization
Page Range: You can adjust the number of pages to scrape by modifying the range in the pages list in the main.py script.
Regex for Experience: The regular expression used to extract years of experience can be further customized in the main.py script.
