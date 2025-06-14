import os
import google.generativeai as genai

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
            "max_output_tokens": 2048,
        }

        # Initialize the generative model.
        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config)

        # Construct the prompt for the LLM.
        # This prompt guides the model to act as a financial analyst.
        prompt = f"""
        As a senior financial analyst, your task is to analyze the following earnings call transcript.
        
        Please perform the following steps:
        1.  Carefully read the entire transcript to understand the company's performance and outlook.
        2.  Extract the most critical financial figures. Focus on:
            - Total Revenue
            - Net Income
            - Earnings Per Share (EPS)
            - Gross Margin (if mentioned)
            - Operating Income (if mentioned)
            - Guidance or outlook for the next quarter/year.
        3.  Identify the key qualitative highlights mentioned by the management. These could be new product launches, strategic partnerships, market trends, or major achievements.
        4.  Identify the main challenges or headwinds the company is facing.
        5.  Synthesize all this information into a concise, easy-to-read summary. The summary should be structured with the following sections:
            - **Financial Highlights:** A bulleted list of the key financial figures.
            - **Key Business Drivers:** A paragraph explaining the main reasons behind the performance.
            - **Challenges & Headwinds:** A paragraph describing any challenges mentioned.
            - **Management Outlook:** A summary of the company's future guidance.
            - **Overall Summary:** A brief, concluding paragraph summarizing the quarter.

        Here is the transcript:
        ---
        {report_text[:15000]} 
        ---
        
        Please provide your analysis based *only* on the text provided.
        """
        
        # We slice the report_text to stay within token limits, focusing on the most important part.
        
        print("Sending request to Gemini API for summarization...")
        response = model.generate_content(prompt)
        
        print("Summary received from API.")
        return response.text

    except Exception as e:
        # Note: For OpenAI, you would use the `openai` library.
        # import openai
        # openai.api_key = api_key
        # response = openai.Completion.create(
        #     engine="text-davinci-003",
        #     prompt=prompt,
        #     max_tokens=1024
        # )
        # return response.choices[0].text.strip()
        return f"An error occurred while contacting the Gemini API: {e}"
