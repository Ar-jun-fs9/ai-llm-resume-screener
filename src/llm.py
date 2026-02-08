"""
LLM module for AI-powered resume summarization using Google Gemini
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

# Load environment variables
load_dotenv()

# Configure Google Generative AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in environment variables. Please set it in your .env file."
    )

# Initialize the model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


def generate_summary(resume_text, job_description, job_role="Data Analyst"):
    """
    Generate a professional AI summary in numbered sections for HTML display.

    Args:
        resume_text (str): Candidate's resume text
        job_description (str): Job description text
        job_role (str): Target job role

    Returns:
        str: AI-generated summary with numbered sections or user-friendly error message
    """
    try:
        prompt = f"""
Please generate a professional AI summary of the candidate in numbered sections (1-5).  

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Instructions:
1. Use numbered sections exactly as:
   1. Candidate Profile Summary
   2. Candidate Fit Assessment for {job_role}
   3. Strengths and Potential Gaps
   4. Actionable Insights for Hiring Decision
   5. Recommendations
2. Write in third person, in paragraph format (no bullet points except in Recommendations).
3. In the Recommendations section, use "• " at the beginning of each recommendation item instead of "-" or numbers.
4. Use plain text only. Do NOT use Markdown formatting (**, _, etc.).
5. Keep the tone professional and suitable for HR reading.
6. Ensure each numbered section heading is followed by a paragraph summarizing the content.
"""

        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        else:
            return "Unable to generate summary. Please try again."

    except ResourceExhausted:
        # Catch quota exceeded (HTTP 429)
        return """
         We're currently unable to generate a summary because the API usage limit has been reached.
         Please contact support via <a href="https://github.com/Ar-jun-fs9" target="_blank">https://github.com/Ar-jun-fs9</a>.
        """

    except Exception as e:
        return f"Error generating summary: {str(e)}"


def generate_quick_summary(resume_text, job_role="Data Analyst"):
    """
    Generate a brief candidate summary in paragraph format.

    Args:
        resume_text (str): Candidate's resume text
        job_role (str): Target job role

    Returns:
        str: Short summary or user-friendly error message
    """
    try:
        prompt = f"""
Provide a brief professional summary of the candidate for {job_role} in paragraph form.  

Resume:
{resume_text}

Instructions:
- Write in third person.
- Keep it concise (2-3 sentences).
- Plain text only, no Markdown formatting.
"""

        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        else:
            return "Unable to generate quick summary."

    except ResourceExhausted:
        # Catch quota exceeded (HTTP 429)
        return "Quick summary cannot be generated right now. API quota exceeded. Please try again later or use a different model."

    except Exception as e:
        return f"Error generating quick summary: {str(e)}"
