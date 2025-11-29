import pytest
from unittest.mock import patch
from django.urls import reverse
from evaluator.models import CV, JobDescription

@pytest.mark.django_db
@patch("evaluator.views.evaluate_cv")
@patch("evaluator.views.generate_recruitment_email")
def test_evaluate_pipeline_with_mocked_llm(mock_email_gen, mock_evaluate_cv, client, cv_files):
    # Create a job to associate with
    job = JobDescription.objects.create(job_title="Test Job", job_requirements="Test Req")
    
    # Set session
    session = client.session
    session['job_id'] = job.id
    session.save()

    # Setup mock return value
    mock_evaluate_cv.return_value = {
        "fit_score": 90,
        "strengths": ["Python", "Django"],
        "weaknesses": [],
        "summary": "Excellent candidate",
        "candidate_name": "Khaled Ahmed"
    }
    
    mock_email_gen.return_value = "Dear Khaled..."
    
    url = reverse("upload_cvs")
import pytest
from unittest.mock import patch
from django.urls import reverse
from evaluator.models import CV, JobDescription

@pytest.mark.django_db
@patch("evaluator.views.evaluate_cv")
@patch("evaluator.views.generate_recruitment_email")
def test_evaluate_pipeline_with_mocked_llm(mock_email_gen, mock_evaluate_cv, client, cv_files):
    # Create a job to associate with
    job = JobDescription.objects.create(job_title="Test Job", job_requirements="Test Req")
    
    # Set session
    session = client.session
    session['job_id'] = job.id
    session.save()

    # Setup mock return value
    mock_evaluate_cv.return_value = {
        "fit_score": 90,
        "strengths": ["Python", "Django"],
        "weaknesses": [],
        "summary": "Excellent candidate",
        "candidate_name": "Khaled Ahmed"
    }
    
    mock_email_gen.return_value = "Dear Khaled..."
    
    url = reverse("upload_cvs")
    data = {"files": cv_files}
    
    # Post the files
    response = client.post(url, data, follow=True)
    
    assert response.status_code == 200
    
    # Check if evaluation was called (it happens in the view loop)
    # Since we upload 3 files, it should be called 3 times
    assert mock_evaluate_cv.call_count == 3

    # Debug: Print filenames
    for obj in CV.objects.all():
        print(f"DEBUG: Saved CV file: {obj.file.name}")

    # Verify that the CV objects have the evaluation data
    cv = CV.objects.first()
    assert cv is not None
    assert cv.fit_score == 90
    assert cv.candidate_name == "Khaled Ahmed"
    assert cv.evaluation_json["summary"] == "Excellent candidate"
