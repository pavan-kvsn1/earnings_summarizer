import sqlite3
import os

# --- Constants ---
DB_FILE = "earnings_reports.db"

# --- Database Initialization ---
def initialize_database():
    """
    Initializes the database and creates tables if they don't exist.
    This function is designed to be safe to call on every run.
    """
    # Check if the database file already exists.
    db_exists = os.path.exists(DB_FILE)
    
    # Connect to the SQLite database.
    # If the file doesn't exist, it will be created.
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # If the database was just created, we need to define the schema.
    if not db_exists:
        print("Database not found. Creating new database file...")
        
        # Create the 'reports' table.
        # This table will store the raw text of the earnings reports.
        cursor.execute('''
            CREATE TABLE reports (
                id INTEGER PRIMARY KEY,
                company TEXT NOT NULL,
                quarter TEXT NOT NULL,
                year INTEGER NOT NULL,
                report_text TEXT,
                UNIQUE(company, quarter, year) -- Ensures no duplicate entries
            )
        ''')
        
        # Create the 'summaries' table.
        # This table will store the AI-generated summaries.
        cursor.execute('''
            CREATE TABLE summaries (
                id INTEGER PRIMARY KEY,
                report_id INTEGER NOT NULL,
                summary_text TEXT NOT NULL,
                FOREIGN KEY (report_id) REFERENCES reports(id)
            )
        ''')
        
        print("Database tables 'reports' and 'summaries' created successfully.")
    
    # Commit the changes and close the connection.
    conn.commit()
    conn.close()

# --- Database Interaction Functions ---

def add_report(company, quarter, year, report_text):
    """
    Adds a new earnings report to the database.

    Args:
        company (str): The name of the company.
        quarter (str): The fiscal quarter (e.g., 'Q1').
        year (int): The fiscal year.
        report_text (str): The full text of the earnings report.

    Returns:
        int: The ID of the newly inserted report.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO reports (company, quarter, year, report_text)
            VALUES (?, ?, ?, ?)
        ''', (company, quarter, year, report_text))
        
        conn.commit()
        report_id = cursor.lastrowid
        print(f"Successfully added report for {company} {quarter} {year} to the database.")
        return report_id
    except sqlite3.IntegrityError:
        print(f"Report for {company} {quarter} {year} already exists in the database.")
        return None
    finally:
        conn.close()


def get_report(company, quarter, year):
    """
    Retrieves an earnings report and its summary from the database.

    Args:
        company (str): The company name.
        quarter (str): The fiscal quarter.
        year (int): The fiscal year.

    Returns:
        tuple: A tuple containing (report_id, report_text, summary_text) or (None, None, None) if not found.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # First, get the report ID and text.
    cursor.execute('''
        SELECT id, report_text FROM reports
        WHERE company = ? AND quarter = ? AND year = ?
    ''', (company, quarter, year))
    
    report_result = cursor.fetchone()
    
    if report_result:
        report_id, report_text = report_result
        
        # Now, check for a summary linked to this report.
        cursor.execute('''
            SELECT summary_text FROM summaries WHERE report_id = ?
        ''', (report_id,))
        
        summary_result = cursor.fetchone()
        summary_text = summary_result[0] if summary_result else None
        
        conn.close()
        return report_id, report_text, summary_text
    
    conn.close()
    return None, None, None


def add_summary(report_id, summary_text):
    """
    Adds a summary for a specific report to the database.

    Args:
        report_id (int): The ID of the report this summary belongs to.
        summary_text (str): The generated summary text.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO summaries (report_id, summary_text)
        VALUES (?, ?)
    ''', (report_id, summary_text))
    
    conn.commit()
    conn.close()
    print(f"Successfully added summary for report ID {report_id} to the database.")

