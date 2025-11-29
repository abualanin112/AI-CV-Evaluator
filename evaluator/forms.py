from django import forms
from .models import JobDescription, CV

class JobForm(forms.ModelForm):
    class Meta:
        model = JobDescription
        fields = ['job_title', 'job_requirements']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Senior Python Developer'}),
            'job_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Paste job description here...'}),
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class CVUploadForm(forms.Form):
    files = MultipleFileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        help_text="Select multiple files (PDF, TXT, MD)"
    )
