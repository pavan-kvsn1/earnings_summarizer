# Earnings Report Summarizer

This project automates the process of fetching, analyzing, and summarizing quarterly earnings reports for public companies.

## Features
- Searches the web for a company's earnings report for a specific quarter and year.
- Downloads and extracts the text content of the report.
- Saves the raw report text in a local SQLite database to avoid re-downloading.
- Uses the Google Gemini API to extract key financial metrics and generate a concise summary.
- Saves the generated summary in the database.
- Command-line interface to easily specify the company, quarter, and year.

## Project Structure
```
earnings-summarizer/ 
├── main.py # Main script to run the application 
├── web_search.py # Handles searching and downloading reports 
├── llm_parser.py # Interacts with the LLM API for parsing and summarizing 
├── database.py # Manages the local SQLite database 
├── requirements.txt # Lists project dependencies 
└── earnings_reports.db # The SQLite database file (will be created on first run)
```

## Setup

1. Clone the repository (or save all the files into a directory named earnings-summarizer).
2. Install Dependencies: Open your terminal, navigate to the project directory, and install the required Python packages.

```pip install -r requirements.txt```

3. Set up the Google Gemini API key:

    - Go to Google AI Studio.
    - Create a new project or select an existing one.
    - Navigate to the API keys section.
    - Create a new API key.
    - Copy the API key and save it in a secure location.
    - Set the API key as an environment variable in your terminal.

    ```export GEMINI_API_KEY=your_api_key``` 
    
    You will need to restart your terminal for the environment variable to take effect.

    You can also set the environment variable in your shell configuration file (e.g., .bashrc, .zshrc) to make it permanent. Alternatiively, the script will prompt you to enter the API key if it is not found in the environment variables.

4. How to run the script:

    Run the main script from the terminal, providing the company name, quarter, and year as arguments.
    Syntax: ```python main.py company quarter year```

    The script will then:
    1. Check if the report already exists in the database.
    2. If the report exists, it will display the summary and exit.
    3. If the report does not exist, it will search for and download the report.
    4. If the report is successfully downloaded, it will use the Google Gemini API to generate a summary.
    5. The summary will be saved to the database and displayed in the terminal.