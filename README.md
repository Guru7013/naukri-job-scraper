# Naukri Job Scraper Using Python & Playwright

## Project Description

This project is a Python-based web scraper that collects job listings from Naukri.com using Playwright.

The scraper collects the following information:

- Job Title
- Company Name
- Location
- Experience
- Skills
- Posted Date
- Job URL

The scraped jobs are stored in an Excel file named `naukri_jobs.xlsx`.

## Technologies Used

- Python
- Playwright
- Pandas
- OpenPyXL
- Microsoft Excel

## Project Features

1. Scrapes job listings from Naukri.com.
2. Extracts important job details.
3. Stores job data in Excel format.
4. Checks existing job URLs before adding new jobs.
5. Prevents duplicate job records.
6. Preserves existing jobs in the Excel file.
7. Creates a log file for error tracking.

## Project Structure

```text
naukri_scraper/
│
├── scraper.py
├── naukri_jobs.xlsx
├── requirements.txt
├── scraper.log
├── README.md
└── venv/