from evaluator.utils.file_parser import extract_text_from_file

def test_extract_text_from_txt(tmp_path):
    p = tmp_path / "t.txt"
    p.write_text("hello world", encoding="utf-8")
    
    # Mocking a Django UploadedFile is tricky with just pathlib, 
    # but our function expects an object with .name and .read() or .open()
    # Let's use SimpleUploadedFile for better simulation
    from django.core.files.uploadedfile import SimpleUploadedFile
    
    with open(p, "rb") as f:
        uploaded_file = SimpleUploadedFile("t.txt", f.read())
        
    text = extract_text_from_file(uploaded_file)
    assert "hello world" in text
