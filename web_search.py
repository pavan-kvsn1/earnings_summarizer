import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def find_and_download_report(company, quarter, year):
    """
    Searches for and downloads the text of an earnings report.

    Args:
        company (str): The name of the company.
        quarter (str): The fiscal quarter (e.g., 'Q1').
        year (int): The fiscal year.

    Returns:
        str: The extracted text of the report, or None if it fails.
    """
    # Construct a search query to find the earnings call transcript.
    # Sites like Motley Fool (fool.com) or Seeking Alpha are often good sources.
    query = f'"{company} ({quarter} {year}) earnings call transcript" site:fool.com'
    print(f"Searching online with query: {query}")

    try:
        # Use DuckDuckGo Search to find relevant links.
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            print("No search results found. Trying a broader search.")
            # Fallback to a more general query if the specific one fails
            query = f'"{company} {quarter} {year} earnings report transcript"'
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))

        if not results:
            print("Could not find any relevant links for the earnings report.")
            return None

        # Attempt to download and parse the first relevant link.
        report_url = results[0]['href']
        print(f"Found potential report link: {report_url}")
        print("Attempting to download and parse...")

        # Use requests to get the HTML content of the page.
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(report_url, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # Use BeautifulSoup to parse the HTML.
        soup = BeautifulSoup(response.content, 'html.parser')

        # This part is highly dependent on the website's structure.
        # We're looking for the main article content.
        # A common pattern is to find a `div` with a class like 'article-body'.
        # This may need adjustment for different websites.
        article_body = soup.find('div', class_='article-body')
        
        if not article_body:
            # Fallback: try to get all paragraph tags as a last resort.
            paragraphs = soup.find_all('p')
            if paragraphs:
                report_text = '\n'.join([p.get_text() for p in paragraphs])
            else:
                 # If no article body or paragraphs found, just get all text
                report_text = soup.get_text(separator='\n', strip=True)
        else:
            report_text = article_body.get_text(separator='\n', strip=True)

        print("Successfully extracted text from the webpage.")
        return report_text

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the webpage: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during web search: {e}")
        return None
