from django.shortcuts import render, redirect, get_object_or_404
from .models import JobDescription, CV
from .forms import JobForm, CVUploadForm
from .utils.file_parser import extract_text_from_file, extract_email, extract_name_fallback
from .utils.vector_db import store_cv_embedding
from .utils.ai_agent import evaluate_cv, rank_candidates
from .utils.email_generator import generate_recruitment_email
import json

def job_entry(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            request.session['job_id'] = job.id
            return redirect('upload_cvs')
    else:
        form = JobForm()
    return render(request, 'evaluator/job_form.html', {'form': form})

def upload_cvs(request):
    job_id = request.session.get('job_id')
    if not job_id:
        return redirect('job_entry')
    
    job = get_object_or_404(JobDescription, id=job_id)

    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            for f in files:
                # 1. Create CV object
                cv = CV.objects.create(job=job, file=f)
                
                # 2. Extract Text
                text = extract_text_from_file(f)
                cv.raw_text = text
                
                # 3. Extract Meta
                cv.candidate_email = extract_email(text)
                cv.candidate_name = extract_name_fallback(text) # Temporary, AI will refine
                
                cv.save()
                
                # 4. Store in Vector DB
                store_cv_embedding(cv.id, text, {"job_id": job_id, "filename": f.name})
            
            return redirect('evaluation_results')
    else:
        form = CVUploadForm()
    
    return render(request, 'evaluator/upload_cvs.html', {'form': form, 'job': job})

def evaluation_results(request):
    job_id = request.session.get('job_id')
    if not job_id:
        return redirect('job_entry')
    
    job = get_object_or_404(JobDescription, id=job_id)
    cvs = CV.objects.filter(job=job)
    
    # Check if we need to run evaluation (if fit_score is 0)
    # In a real app, this might be a background task. Here we do it inline.
    # Parallelize AI evaluation
    from concurrent.futures import ThreadPoolExecutor, as_completed

    cvs_to_evaluate = [cv for cv in cvs if not cv.evaluation_json]
    
    if cvs_to_evaluate:
        print(f"DEBUG: Starting AI evaluation for {len(cvs_to_evaluate)} CVs in parallel...")
        
        def process_cv(cv):
            print(f"DEBUG: Evaluating CV {cv.id}...")
            result = evaluate_cv(job.job_requirements, cv.raw_text)
            return cv, result

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_cv = {executor.submit(process_cv, cv): cv for cv in cvs_to_evaluate}
            
            for future in as_completed(future_to_cv):
                cv = future_to_cv[future]
                try:
                    eval_result = future.result()
                    # Unpack if needed, but here result is (cv, eval_result) tuple from helper? 
                    # Ah, helper returns (cv, result)
                    _, data = eval_result
                    
                    cv.evaluation_json = data
                    cv.fit_score = data.get('fit_score', 0)
                    
                    ai_name = data.get('candidate_name')
                    if ai_name and ai_name != "Unknown":
                        cv.candidate_name = ai_name
                    
                    cv.save()
                    print(f"DEBUG: Finished CV {cv.id}")
                except Exception as exc:
                    print(f"DEBUG: CV {cv.id} generated an exception: {exc}")
    
    # Rank candidates
    ranked_cvs = rank_candidates(list(cvs))
    
    # Generate email for top candidate
    top_candidate_email_draft = ""
    if ranked_cvs:
        top_candidate = ranked_cvs[0]
        top_candidate_email_draft = generate_recruitment_email(
            top_candidate.candidate_name,
            job.job_title,
            top_candidate.candidate_email
        )

    return render(request, 'evaluator/evaluation_results.html', {
        'job': job,
        'cvs': ranked_cvs,
        'email_draft': top_candidate_email_draft
    })
