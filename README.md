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
