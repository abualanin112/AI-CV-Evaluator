import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from django.conf import settings

def get_llm():
    return ChatGoogleGenerativeAI(
        google_api_key=settings.GOOGLE_API_KEY,
        model=settings.GEMINI_MODEL,
        temperature=0.2
    )

def evaluate_cv(job_requirements, cv_text):
    """
    Evaluates a single CV against job requirements.
    Returns a JSON object with fit_score, strengths, weaknesses, summary.
    """
    llm = get_llm()
    
    prompt_template = """
    You are an expert HR Recruiter. Evaluate the following Candidate CV against the Job Requirements.
    
    JOB REQUIREMENTS:
    {job_requirements}
    
    CANDIDATE CV:
    {cv_text}
    
    Output strictly valid JSON in the following format:
    {{
        "fit_score": <integer between 0 and 100>,
        "strengths": ["strength1", "strength2", ...],
        "weaknesses": ["weakness1", "weakness2", ...],
        "summary": "<short professional summary>",
        "candidate_name": "<extracted name from CV>"
    }}
    """
    
    prompt = PromptTemplate(
        input_variables=["job_requirements", "cv_text"],
        template=prompt_template
    )
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({"job_requirements": job_requirements, "cv_text": cv_text})
        content = response.content
        
        # Clean up code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
            
        return json.loads(content.strip())
    except Exception as e:
        print(f"Error in AI evaluation: {e}")
        error_msg = "Error during evaluation"
        summary_msg = "Could not evaluate due to an error."
        
        # Check for rate limit error string if class not available or just to be safe
        if "insufficient_quota" in str(e) or "RateLimitError" in str(e):
            error_msg = "Quota Exceeded"
            summary_msg = "OpenAI API Quota Exceeded. Please check your billing."

        return {
            "fit_score": 0,
            "strengths": [],
            "weaknesses": [error_msg],
            "summary": summary_msg,
            "candidate_name": "Unknown"
        }

def rank_candidates(cv_list):
    """
    Sorts a list of CV objects based on fit_score.
    """
    return sorted(cv_list, key=lambda x: x.fit_score, reverse=True)
