import re
import pdfplumber
import markdown
import os

def extract_text_from_file(uploaded_file):
    """
    Extracts text from an uploaded file (PDF, TXT, MD).
    Returns the extracted text string.
    """
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    text = ""

    try:
        # Ensure we are at the beginning of the file
        if hasattr(uploaded_file, 'seek'):
            uploaded_file.seek(0)
            
        if file_extension == '.pdf':
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        
        elif file_extension == '.txt':
            text = uploaded_file.read().decode('utf-8')
            
        elif file_extension == '.md':
            md_content = uploaded_file.read().decode('utf-8')
            # Convert MD to HTML then maybe text, or just treat as text. 
            # For CV analysis, raw markdown is often better as it preserves structure.
            # But let's strip HTML tags if any.
            text = md_content 
            
        else:
            # Fallback for other text-based formats
            try:
                text = uploaded_file.read().decode('utf-8')
            except:
                text = "[Error: Unsupported file format or encoding]"

    except Exception as e:
        print(f"Error reading file {uploaded_file.name}: {e}")
        return ""

    return text

def extract_email(text):
    """
    Extracts the first found email address using Regex.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    if match:
        return match.group(0)
    return None

def extract_name_fallback(text):
    """
    Simple heuristic to guess a name if AI fails or as a pre-check.
    Usually the first line or lines of a CV.
    """
    lines = text.strip().split('\n')
    for line in lines[:5]: # Check first 5 lines
        clean_line = line.strip()
        if clean_line and len(clean_line.split()) < 5: # Likely a name if short
            return clean_line
    return "Unknown Candidate"
