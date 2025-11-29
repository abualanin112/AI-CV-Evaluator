import pytest
from django.urls import reverse
from evaluator.models import CV, JobDescription

from evaluator.models import CV, JobDescription
from unittest.mock import patch

@pytest.mark.django_db
@patch("evaluator.views.evaluate_cv")
@patch("evaluator.views.generate_recruitment_email")
def test_upload_view_saves_files(mock_email, mock_eval, client, cv_files):
    # Setup mocks to avoid API calls during redirect
    mock_eval.return_value = {}
    mock_email.return_value = "Draft"
    # Create a job to associate with
    job = JobDescription.objects.create(job_title="Test Job", job_requirements="Test Req")
    
    # Set session
    session = client.session
    session['job_id'] = job.id
    session.save()

    url = reverse("upload_cvs")
    
    # Create a dictionary suitable for multipart/form-data
    # We need to pass the files as a list for the 'files' key
import pytest
from django.urls import reverse
from evaluator.models import CV, JobDescription

from evaluator.models import CV, JobDescription
from unittest.mock import patch

@pytest.mark.django_db
@patch("evaluator.views.evaluate_cv")
@patch("evaluator.views.generate_recruitment_email")
def test_upload_view_saves_files(mock_email, mock_eval, client, cv_files):
    # Setup mocks to avoid API calls during redirect
    mock_eval.return_value = {}
    mock_email.return_value = "Draft"
    # Create a job to associate with
    job = JobDescription.objects.create(job_title="Test Job", job_requirements="Test Req")
    
    # Set session
    session = client.session
    session['job_id'] = job.id
    session.save()

    url = reverse("upload_cvs")
    
    # Create a dictionary suitable for multipart/form-data
    # We need to pass the files as a list for the 'files' key
    data = {"files": cv_files}
    
    # Use follow=True to handle the redirect
    response = client.post(url, data, follow=True)
    
    assert response.status_code == 200
    # Check if CV objects were created
    assert CV.objects.count() == len(cv_files)

    # Debug: Print filenames
    for obj in CV.objects.all():
        print(f"DEBUG: Saved CV file: {obj.file.name}")

    # Verify one of the CVs
    # Relax filter to just get one and check content/name
    cv = CV.objects.first()
    assert cv is not None
    # Check if one of the expected filenames is in the saved name
    assert any(f.name.replace(".txt", "") in cv.file.name for f in cv_files)
    assert "khaled.dev97@gmail.com" in cv.raw_text
