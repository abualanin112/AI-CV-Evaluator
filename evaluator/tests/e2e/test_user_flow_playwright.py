import pytest
from pathlib import Path
from django.urls import reverse

import os
# Allow async unsafe operations for Playwright + Django live_server interaction
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# Use 'live_server' fixture from pytest-django to run a live server
def test_user_flow_playwright(page, live_server):
    # 1. Go to Job Entry Page
    page.goto(live_server.url + reverse("job_entry"))
    
    # 2. Fill Job Form
    page.fill("input[name='job_title']", "Full Stack Developer")
    page.fill("textarea[name='job_requirements']", "React, Django, REST APIs, Docker")
    page.click("button[type='submit']")
    
    # 3. Upload CVs Page
    # Verify we are redirected to upload page
    assert "/upload/" in page.url
    
    # Prepare file path
    base_path = Path(__file__).resolve().parent.parent / "fixtures"
    file_path = base_path / "khaled_ahmed.txt"
    
    # Upload file
    # Note: The input name in our form is 'files'
    page.set_input_files("input[name='files']", str(file_path))
    
    # Click Upload
    page.click("button[type='submit']")
    
    # 4. Evaluation Results Page
    # Wait for redirection to results
    # The URL path is /results/, so we wait for that
    page.wait_for_url("**/results/")
    
    # Check if we have results (using card-header since card-title isn't used)
    assert page.locator(".card-header").count() > 0
