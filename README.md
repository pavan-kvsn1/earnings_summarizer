Earnings Report Summarizer
This project automates the process of fetching, analyzing, and summarizing quarterly earnings reports for public companies.

Features
Searches the web for a company's earnings report for a specific quarter and year.

Downloads and extracts the text content of the report.

Saves the raw report text in a local SQLite database to avoid re-downloading.

Uses the Google Gemini API to extract key financial metrics and generate a concise summary.

Saves the generated summary in the database.

Command-line interface to easily specify the company, quarter, and year.

Project Structure
earnings-summarizer/
├── main.py             # Main script to run the application
├── web_search.py       # Handles searching and downloading reports
├── llm_parser.py       # Interacts with the LLM API for parsing and summarizing
├── database.py         # Manages the local SQLite database
├── requirements.txt    # Lists project dependencies
└── earnings_reports.db # The SQLite database file (will be created on first run)

Setup
Clone the repository (or save all the files into a directory named earnings-summarizer).

Install Dependencies:
Open your terminal, navigate to the project directory, and install the required Python packages.

pip install -r requirements.txt

Get a Google Gemini API Key:

Go to Google AI Studio.

Sign in and click on "Get API key".

Copy the generated API key.

Set Environment Variable:
It's recommended to set your API key as an environment variable for security.

macOS/Linux:

export GEMINI_API_KEY="YOUR_API_KEY"

Windows (Command Prompt):

set GEMINI_API_KEY="YOUR_API_KEY"

Windows (PowerShell):

$env:GEMINI_API_KEY="YOUR_API_KEY"

You can also add this line to your shell's startup file (e.g., .bashrc, .zshrc) to make it permanent. Alternatively, the script will prompt you to enter the key if the environment variable is not found.

How to Run
Run the main script from your terminal, providing the company name, quarter, and year as arguments.

Syntax:

python main.py "Company Name" Q<number> <year>

Example:

python main.py "NVIDIA" Q1 2024

The script will then:

Check the local database for an existing report.

If not found, it will search online, download the report, and save it.

It will then use the Gemini API to generate and display a summary.

The summary will also be saved to the database for future access.
