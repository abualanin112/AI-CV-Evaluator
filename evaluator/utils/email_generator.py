from .ai_agent import get_llm
from langchain_core.prompts import PromptTemplate

def generate_recruitment_email(candidate_name, job_title, candidate_email):
    """
    Generates a professional email for the top candidate.
    """

    llm = get_llm()  # Should return ChatGoogleGenerativeAI instance

    prompt_template = """
You are Sarah Jenkins, the HR Manager at 'TechNova Solutions'. Write a formal and encouraging email to a successful candidate who has been shortlisted for an interview.

Candidate Name: {candidate_name}
Job Title: {job_title}

Use the following realistic details in the email instead of placeholders:
- Company Name: TechNova Solutions
- Sender Name: Sarah Jenkins
- Contact Info: +1 (555) 012-3456 | hr@technova.com
- Location: 45 Innovation Blvd, Tech District (or via Google Meet)

The email should be ready to send. You can leave a placeholder ONLY for the specific Date and Time of the interview, but everything else should be filled with the fake data provided.

Return ONLY the email text.
"""

    prompt = PromptTemplate(
        input_variables=["candidate_name", "job_title"],
        template=prompt_template
    )

    chain = prompt | llm

    # For ChatOpenAI, response is an object with ".content"
    try:
        response = chain.invoke({
            "candidate_name": candidate_name,
            "job_title": job_title
        })
        return response.content
    except Exception as e:
        print(f"Error generating email: {e}")
        return "Could not generate email due to an error (e.g., quota exceeded)."
