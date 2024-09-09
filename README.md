# Job Scraper for SAP Careers

This project is an asynchronous web scraper designed to extract job details from the SAP careers website. The script fetches job postings, extracts relevant details, and saves them in a structured JSON format.

## Features

- **Asynchronous Scraping:** Efficiently fetches multiple job pages simultaneously using `aiohttp` and `asyncio`.
- **BeautifulSoup Integration:** Parses the HTML content of job pages to extract necessary details.
- **Years of Experience Extraction:** Extracts the number of years of experience required from job descriptions using regular expressions.
- **Duplicate Filtering:** Ensures that no duplicate job entries are saved in the final JSON file.
- **JSON Output:** Saves the scraped job data in a neatly formatted JSON file.

## Project Structure

