from evaluator.utils.file_parser import extract_email

def test_extract_email_simple():
    text = "Name: Khaled Ahmed\nEmail: khaled.dev97@gmail.com\n"
    email = extract_email(text)
    assert email == "khaled.dev97@gmail.com"

def test_no_email_returns_none():
    text = "No contact here"
    email = extract_email(text)
    assert email is None
