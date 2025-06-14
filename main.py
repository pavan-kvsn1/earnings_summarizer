import argparse
import os
import sys
from getpass import getpass

# Import our custom modules
import database
import web_search
import llm_parser

def main():
    """
    Main function to orchestrate the earnings report summarization process.
    """
    # --- 1. Initialize Database ---
    # Ensure the database and its tables exist before we do anything else.
    database.initialize_database()

    # --- 2. Setup Argument Parser ---
    # This allows us to run the script with command-line arguments.
    parser = argparse.ArgumentParser(
        description="A tool to find, download, and summarize quarterly earnings reports."
    )
    parser.add_argument("company", type=str, help="The name of the company (e.g., 'NVIDIA').")
    parser.add_argument("quarter", type=str, help="The fiscal quarter (e.g., 'Q1').")
    parser.add_argument("year", type=int, help="The fiscal year (e.g., 2024).")
    
    # If no arguments are provided, show the help message and exit.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()
    
    company = args.company
    quarter = args.quarter.upper()
    year = args.year
    
    print("-" * 50)
    print(f"Starting process for: {company} {quarter} {year}")
    print("-" * 50)

    # --- 3. Check Database for Existing Report and Summary ---
    print("Checking local database for existing report...")
    report_id, report_text, summary_text = database.get_report(company, quarter, year)
    
    # If we have a summary, we can just print it and exit.
    if summary_text:
        print("\nFound a pre-existing summary in the database. Displaying it now:\n")
        print("+" * 50)
        print(summary_text)
        print("+" * 50)
        print("\nProcess finished.")
        return # Exit the function

    # If we have the report text but no summary, we can skip the download step.
    if report_text:
        print("Found report text in the database, but no summary. Proceeding to summarization.")
    else:
        # --- 4. Search and Download Report (if not in DB) ---
        print("\nReport not found in database. Searching online...")
        report_text = web_search.find_and_download_report(company, quarter, year)
        
        if not report_text:
            print(f"\nCould not retrieve the earnings report for {company} {quarter} {year}. Exiting.")
            return

        # Save the newly downloaded report to the database.
        report_id = database.add_report(company, quarter, year, report_text)
        if not report_id:
            print("\nFailed to add the report to the database. Exiting.")
            return

    # --- 5. Summarize with LLM ---
    print("\nProceeding to generate summary with Gemini API...")
    
    # Get the API key from an environment variable or prompt the user.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("\nGEMINI_API_KEY environment variable not found.")
        try:
            api_key = getpass("Please enter your Google Gemini API Key: ")
        except (IOError, EOFError):
             print("\nCould not read API key. Exiting.")
             return


    if not api_key:
        print("\nAPI Key is required to generate a summary. Exiting.")
        return

    # Call the LLM parser to get the summary.
    summary = llm_parser.get_gemini_summary(report_text, api_key)

    # --- 6. Display and Save Summary ---
    if summary and "An error occurred" not in summary:
        print("\n--- Generated Summary ---")
        print(summary)
        print("-------------------------\n")
        
        # Save the new summary to the database.
        database.add_summary(report_id, summary)
    else:
        print("\nFailed to generate a summary.")
        print(f"Reason: {summary}")
    
    print("Process finished.")


if __name__ == "__main__":
    main()
