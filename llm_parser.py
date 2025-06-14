import os
import google.generativeai as genai

SECTION_SUMMARY_PROMPT = """
As a financial analyst, your task is to summarize the following section from an earnings report.
Focus *only* on the information present in this specific section.

Please identify and extract:
1.  Key financial figures or quantitative performance indicators mentioned.
2.  Key qualitative points, achievements, product updates, or strategic initiatives discussed.
3.  Any challenges, risks, or headwinds highlighted.
4.  If this section discusses future outlook, guidance, or forward-looking statements, please note that.

Provide a concise and clear summary of this section.
---
Section Text:
{section_text}
---
Summary:
"""

def get_gemini_summary(report_text, api_key):
    """
    Uses the Google Gemini API to summarize an earnings report.

    Args:
        report_text (str): The full text of the earnings report.
        api_key (str): The API key for the Gemini API.

    Returns:
        str: The AI-generated summary, or an error message.
    """
    try:
        # Configure the Gemini API with the provided key.
        genai.configure(api_key=api_key)

        # Set up the model generation configuration.
        generation_config = {
            "temperature": 0.2,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 1024, # Adjusted for section summaries
        }

        # Initialize the generative model.
        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config)

        sections = split_into_sections(report_text)

        if not sections or (len(sections) == 1 and not sections[0].strip()):
            return "Report text is too short or has no identifiable sections."

        section_summaries = []
        MAX_SECTION_LENGTH = 15000

        for i, section_text in enumerate(sections):
            if not section_text.strip():
                section_summaries.append(f"--- Section {i+1} (empty) ---")
                continue

            truncated_text = section_text
            if len(section_text) > MAX_SECTION_LENGTH:
                truncated_text = section_text[:MAX_SECTION_LENGTH] + "\n[Section truncated due to length]"

            # Use the new detailed prompt for summarizing a section
            prompt = SECTION_SUMMARY_PROMPT.format(section_text=truncated_text)

            try:
                print(f"Sending request to Gemini API for summarizing section {i+1}...")
                response = model.generate_content(prompt)
                summary = response.text
                section_summaries.append(f"--- Section {i+1} Summary ---")
                section_summaries.append(summary)
                print(f"Summary received for section {i+1}.")
            except Exception as section_e:
                error_message = f"Could not summarize section {i+1}: {section_text[:50]}..."
                print(f"Error summarizing section {i+1}: {section_e}")
                section_summaries.append(f"--- Section {i+1} Error ---")
                section_summaries.append(error_message)
        
        return "\n\n".join(section_summaries)

    except Exception as e:
        # General errors (e.g., API key issue, model initialization)
        print(f"An overall error occurred in get_gemini_summary: {e}")
        return f"An error occurred: {e}"


def split_into_sections(report_text: str) -> list[str]:
    """
    Splits an earnings report into sections based on common headers.

    Args:
        report_text (str): The full text of the earnings report.

    Returns:
        list[str]: A list of strings, where each string is the text of a section.
                   Returns the original report_text as a single section if no headers are found.
    """
    section_headers = [
        "Financial Results",
        "Management Discussion",
        "Outlook",
        "Key Highlights",
        "Q&A",
        "Conference Call",
        "Financial Statements",
        "Results of Operations",
        "Business Overview",
        "Risk Factors"
    ]

    # Normalize headers to lowercase for case-insensitive matching
    normalized_headers = [header.lower() for header in section_headers]

    sections = []
    current_section_lines = []
    lines = report_text.splitlines() # splitlines() keeps empty strings for blank lines

    header_found_yet = False # Tracks if we've encountered the first header

    for line in lines:
        stripped_line = line.strip()
        is_header = False
        # Check if the line starts with any of the predefined headers (case-insensitive)
        # Only consider it a header if the stripped line is not empty (i.e. line itself wasn't just spaces)
        if stripped_line and any(stripped_line.lower().startswith(h) for h in normalized_headers):
            is_header = True

        if is_header:
            if current_section_lines: # Process previous block
                processed_section_text = "\n".join(current_section_lines)
                if not header_found_yet: # This was pre-header content
                    processed_section_text = processed_section_text.strip()
                else: # This was a regular section that started with a header, just rstrip
                    processed_section_text = processed_section_text.rstrip()

                if processed_section_text: # Add if not empty after processing
                    sections.append(processed_section_text)

            current_section_lines = [line] # Start new section with the raw header line
            header_found_yet = True
        else:
            current_section_lines.append(line)

    # Add the last processed section
    if current_section_lines:
        processed_section_text = "\n".join(current_section_lines)
        if not header_found_yet: # This was pre-header content or the only content
            processed_section_text = processed_section_text.strip()
        else: # This was the last section, started by a header, just rstrip
            processed_section_text = processed_section_text.rstrip()

        if processed_section_text: # Add if not empty after processing
            sections.append(processed_section_text)

    # Handle cases where report_text itself was empty or only whitespace
    if not sections and not report_text.strip():
        return []

    return sections
