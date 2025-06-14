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
    # --- MODIFIED FOR TESTING ---
    # Bypassing database check and web search for llm_parser testing
    print("Bypassing database check and web search for direct llm_parser testing.")

    dummy_report_text = f"""
    **Alphabet (GOOGL) Q1 2023 Earnings Call Transcript**

    **Company Participants**

    *   Jim Friedland – Director, Investor Relations
    *   Sundar Pichai – Chief Executive Officer
    *   Philipp Schindler – Senior Vice President and Chief Business Officer
    *   Ruth Porat – Senior Vice President and Chief Financial Officer

    **Operator**

    Welcome, everyone. Thank you for standing by for the Alphabet First Quarter 2023 Earnings Conference Call.
    We have a lot to cover today, so let's get started.

    **Financial Results**

    In Q1 2023, Alphabet reported total revenues of $69.8 billion, an increase of 3% year-over-year.
    Search and other revenues were $40.3 billion, up 2%. YouTube advertising revenues were $6.7 billion, down 3%.
    Google Cloud revenues were $7.4 billion, up 28%.
    Net income was $15.05 billion, and diluted earnings per share were $1.17.
    Operating margin was 25%. We are pleased with these results given the current economic climate.
    Our investments in AI are starting to pay off significantly in Search and Cloud.

    **Management Discussion**

    Sundar Pichai speaking:
    This quarter, our performance was solid. We are particularly encouraged by the momentum in our Cloud segment.
    We continue to invest heavily in AI across the board, and the innovations are driving user engagement and new opportunities for monetization.
    The economic environment remains challenging, but we are navigating it well by focusing on delivering value for our users and partners.
    Pixel family of devices also saw good growth this quarter.

    Philipp Schindler speaking:
    Advertiser spending is stabilizing, though some sectors remain cautious. We are working closely with our advertisers to help them achieve their goals.
    Retail, travel, and finance were key drivers for Search revenue. YouTube Shorts monetization is progressing well.

    Ruth Porat speaking:
    We are maintaining disciplined expense management. Headcount growth has slowed considerably as we focus on optimizing our operations.
    Capital expenditures were primarily for our technical infrastructure to support AI development and Cloud growth.
    Share repurchases amounted to $15 billion this quarter.

    **Outlook**

    For Q2 2023, we expect continued modest revenue growth. We anticipate that the current trends in Search and YouTube advertising will persist.
    Google Cloud is expected to maintain its strong growth trajectory.
    We are committed to our long-term AI strategy and believe it will be a key driver of future growth.
    Regulatory scrutiny remains a factor we are actively managing across various jurisdictions.
    We project operating expenses to further moderate throughout the year.

    **Key Highlights**

    *   Launched new AI features in Google Search, enhancing user experience.
    *   Google Cloud Platform (GCP) secured several large enterprise contracts.
    *   Significant advancements in our Large Language Models (LLMs), including PaLM 2.
    *   Continued growth in YouTube Shorts viewership and initial monetization efforts.
    *   Pixel device sales showed strong year-over-year growth.

    **Q&A**

    Question 1: Analyst from Morgan Stanley
    Can you elaborate on the competitive landscape in Cloud?
    Answer: (Sundar Pichai) We believe our focus on AI-differentiated services and our multi-cloud strategy are key advantages. Customer feedback has been very positive.

    Question 2: Analyst from Goldman Sachs
    What are the early results from AI in Search?
    Answer: (Sundar Pichai) Early signals are very promising. Users are engaging more deeply, and we are seeing improvements in query satisfaction. We are rolling out features thoughtfully.

    Question 3: Analyst from JP Morgan
    How do you see the regulatory environment evolving?
    Answer: (Ruth Porat) We are actively engaged with regulators globally and are committed to complying with all applicable laws while continuing to innovate. It's a dynamic environment.

    This concludes our earnings call. Thank you for joining us.
    """
    report_text = dummy_report_text
    # Assign a dummy report_id for testing purposes if add_summary needs it
    report_id = database.add_report(company, quarter, year, report_text) # Still add to DB for this run
    if not report_id:
        print("\nFailed to add the dummy report to the database. Exiting.")
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
