import os
import json
from flask import Flask, request, jsonify, render_template, make_response
from dotenv import load_dotenv
# import openai # Uncomment this if using the real OpenAI API

# --- Configuration ---
load_dotenv() # Load environment variables from .env file
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')

# --- OpenAI Configuration (Placeholder vs Real) ---
USE_REAL_OPENAI = False # <<< SET TO True TO USE REAL API (requires API Key in .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# if USE_REAL_OPENAI:
#     if not OPENAI_API_KEY:
#         print("ERROR: OPENAI_API_KEY not found in .env file. Set USE_REAL_OPENAI = False to use placeholder.")
#         # You might want to exit or handle this more gracefully
#     try:
#         openai.api_key = OPENAI_API_KEY
#         # Test connection (optional)
#         # client = openai.OpenAI() # Initialize client if needed for newer versions
#         print("OpenAI client configured.")
#     except Exception as e:
#         print(f"Error configuring OpenAI: {e}")
#         USE_REAL_OPENAI = False # Fallback to placeholder if config fails

# --- Routes ---
@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/rewrite', methods=['POST'])
def rewrite_cv_route():
    """Handles the CV rewriting request."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Extract data from request
    cv_data = {
        "summary": data.get('summary', ''),
        "experience1": data.get('experience1', ''),
        "experience2": data.get('experience2', ''),
        "education": data.get('education', ''),
        "skills": data.get('skills', ''),
        "languages": data.get('languages', ''),
        "additional": data.get('additional', ''),
    }
    job_desc = data.get('job_description', '')
    company = data.get('company', '')
    industry = data.get('industry', '')
    tone = data.get('tone', 'Keep original style')

    if not job_desc:
         return jsonify({"error": "Job Description cannot be empty"}), 400

    try:
        if USE_REAL_OPENAI:
            # --- REAL OPENAI API CALL ---
            # rewritten_text = call_openai_api(cv_data, job_desc, company, industry, tone)
            # For now, we'll just return the placeholder response even if USE_REAL_OPENAI is True
            # Replace the line below with the actual call_openai_api function call when ready
            print("Simulating OpenAI call...")
            rewritten_text = generate_placeholder_rewrite(cv_data, job_desc, company, industry, tone)
            print("Simulation complete.")
        else:
            # --- PLACEHOLDER LOGIC ---
            print("Using placeholder rewrite logic...")
            rewritten_text = generate_placeholder_rewrite(cv_data, job_desc, company, industry, tone)
            print("Placeholder generation complete.")

        return jsonify({"rewritten_cv": rewritten_text})

    except Exception as e:
        print(f"Error during rewrite: {e}") # Log the error server-side
        # Consider logging traceback: import traceback; traceback.print_exc()
        return jsonify({"error": f"An internal error occurred: {e}"}), 500

# --- Helper Functions ---

def generate_placeholder_rewrite(cv_data, job_desc, company, industry, tone):
    """Generates a placeholder rewritten CV for testing."""
    output = f"--- Rewritten CV for {company} ({industry}) ---\n\n"
    output += f"Tone Adaptation: {tone}\n"
    output += f"Based on Job Description Keywords (e.g., from first 50 chars): '{job_desc[:50]}...'\n"
    output += "-----------------------------------------------\n\n"

    output += "**Professional Summary**\n"
    output += f"[Rewritten based on job keywords] {cv_data['summary']}\n\n"

    output += "**Experience**\n"
    output += f"Experience 1:\n[Rephrased to highlight relevant skills] {cv_data['experience1']}\n\n"
    if cv_data['experience2']:
        output += f"Experience 2:\n[Rephrased to highlight relevant skills] {cv_data['experience2']}\n\n"

    output += "**Education**\n"
    output += f"[Formatted] {cv_data['education']}\n\n"

    output += "**Skills**\n"
    output += f"[Keywords added/emphasized] {cv_data['skills']}\n\n"

    output += "**Languages**\n"
    output += f"{cv_data['languages']}\n\n"

    if cv_data['additional']:
        output += "**Additional Sections**\n"
        output += f"[Reviewed for relevance] {cv_data['additional']}\n\n"

    output += "--- End of Rewritten CV (Placeholder) ---"
    import time
    time.sleep(1) # Simulate processing time
    return output

def call_openai_api(cv_data, job_desc, company, industry, tone):
    """
    Calls the OpenAI API to rewrite the CV.
    (This is the function you would implement fully)
    """
    # IMPORTANT: You need to install and import the openai library first
    # pip install openai
    # import openai

    # Ensure the client is initialized (might need adjustment based on openai lib version)
    # client = openai.OpenAI() # for openai >= 1.0

    prompt = construct_openai_prompt(cv_data, job_desc, company, industry, tone)

    try:
        print("--- Sending Prompt to OpenAI ---")
        # print(prompt) # Uncomment to debug the prompt
        print("-----------------------------")

        # Example using ChatCompletion (adjust model and parameters as needed)
        # Requires openai library v1.0+
        # response = client.chat.completions.create(
        #      model="gpt-3.5-turbo", # Or "gpt-4" etc.
        #      messages=[
        #          {"role": "system", "content": "You are an expert CV writer helping job seekers tailor their CV to specific job descriptions."},
        #          {"role": "user", "content": prompt}
        #      ],
        #      temperature=0.7, # Adjust for creativity vs precision
        #      max_tokens=1500 # Adjust based on expected output length
        # )

        # --- MOCK RESPONSE FOR WHEN `USE_REAL_OPENAI` is True but no API call made yet ---
        # Remove this mock response structure when implementing the actual API call above
        mock_response_content = generate_placeholder_rewrite(cv_data, job_desc, company, industry, tone)
        mock_response_content = mock_response_content.replace("(Placeholder)", "(Simulated OpenAI Response)")
        print("--- Received Simulated OpenAI Response ---")
        return mock_response_content
        # --- END MOCK RESPONSE ---


        # --- Process REAL response (when uncommenting the API call) ---
        # rewritten_text = response.choices[0].message.content.strip()
        # print("--- Received OpenAI Response ---")
        # print(rewritten_text)
        # print("-----------------------------")
        # return rewritten_text
        # --- END REAL response processing ---


    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        # Consider more specific error handling based on OpenAI exceptions
        return f"Error during OpenAI processing: {e}" # Or raise the exception


def construct_openai_prompt(cv_data, job_desc, company, industry, tone):
    """Constructs the detailed prompt for the OpenAI API."""

    prompt = f"""
    Rewrite the following CV sections to be highly tailored for a job application at '{company}' in the '{industry}' industry, based on the provided Job Description.

    **Rules:**
    1.  **Integrate Keywords:** Seamlessly weave relevant keywords and skills mentioned in the Job Description into the CV sections.
    2.  **Maintain Facts:** Absolutely preserve the core facts, experiences, dates, and job titles from the original CV sections. Do NOT invent qualifications, experiences, or skills.
    3.  **Rephrase & Reorganize:** Rephrase sentences and potentially reorganize bullet points within sections (like Experience) to better highlight alignment with the job requirements.
    4.  **Professional Language:** Use clear, concise, and professional language suitable for a CV.
    5.  **Tone Adaptation:** { 'Adapt the writing style and tone to mirror the tone of the Job Description.' if tone == 'Adapt to job offer tone' else 'Maintain a professional tone consistent with the original CV sections.' }
    6.  **Output Format:** Present the rewritten CV clearly, with each section clearly labeled (e.g., **Professional Summary**, **Experience**, **Education**, **Skills**, **Languages**, **Additional Sections**). Ensure the output is plain text suitable for copying.

    **Job Description:**
    ---
    {job_desc}
    ---

    **Original CV Sections:**
    ---
    **Professional Summary:**
    {cv_data['summary']}

    **Experience 1:**
    {cv_data['experience1']}

    **Experience 2:**
    {cv_data['experience2']}

    **Education:**
    {cv_data['education']}

    **Skills:**
    {cv_data['skills']}

    **Languages:**
    {cv_data['languages']}

    **Additional Sections:**
    {cv_data['additional']}
    ---

    **Rewritten CV Output:**
    """
    return prompt.strip()


# --- Main Execution ---
if __name__ == '__main__':
    # Port 5001 is often free, change if needed
    app.run(debug=True, port=5001)