import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path

BASE = Path(__file__).resolve().parent
FIX = BASE / "fixtures"

@pytest.fixture
def cv_files():
    files = []
    # Ensure these files exist in fixtures directory
    for name in ["khaled_ahmed.txt", "omar_mahmoud.txt", "mariam_saad.txt"]:
        path = FIX / name
        if path.exists():
            with open(path, "rb") as fh:
                files.append(SimpleUploadedFile(name, fh.read(), content_type="text/plain"))
    return files
