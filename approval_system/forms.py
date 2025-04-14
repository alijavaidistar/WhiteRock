
from django import forms
import json
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['form_name', 'signature']  # ✅ 'data' is handled separately in clean()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get logged-in user
        super().__init__(*args, **kwargs)

        form_name = self.initial.get('form_name', '')

        print(f"🚀 Initializing Form: {form_name}")  # Debugging

        #  If form_name is missing, try setting it from POST data
        if not form_name and 'form_name' in self.data:
            form_name = self.data.get('form_name', '')

        if form_name == "Term Withdrawal Request":
            self.fields['student_name'] = forms.CharField(label="Student Name", required=True)
            self.fields['myuh_id'] = forms.CharField(label="myUH ID", required=True)
            self.fields['last_name'] = forms.CharField(label="Last Name", initial=user.last_name if user else '', required=True)
            self.fields['first_name'] = forms.CharField(label="First Name", initial=user.first_name if user else '', required=True)
            self.fields['middle_name'] = forms.CharField(label="Middle Name", required=False)
            self.fields['phone'] = forms.CharField(label="Phone #", required=True)
            self.fields['email'] = forms.EmailField(label="Email", initial=user.email if user else '', disabled=True)
            self.fields['program_plan'] = forms.CharField(label="Program/Plan", required=True)
            self.fields['academic_career'] = forms.ChoiceField(
                choices=[('Undergraduate', 'Undergraduate'), ('Graduate', 'Graduate')],
                widget=forms.Select,
                label="Academic Career"
            )
            self.fields['withdrawal_term'] = forms.ChoiceField(
                choices=[('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer')],
                widget=forms.RadioSelect,
                label="Withdrawal Term"
            )

        elif form_name == "Veteran Educational Benefits":
            print("✅ Adding Veteran Benefits fields...")  # Debugging
            self.fields['first_name'] = forms.CharField(label="First Name", required=True)
            self.fields['last_name'] = forms.CharField(label="Last Name", required=True)
            self.fields['phone'] = forms.CharField(label="Phone", required=True)
            self.fields['academic_career'] = forms.ChoiceField(
                choices=[('Undergraduate', 'Undergraduate'), ('Graduate', 'Graduate')],
                widget=forms.Select,
                label="Academic Career"
            )
            self.fields['va_chapter'] = forms.ChoiceField(
                choices=[('31', 'Chapter 31'), ('35', 'Chapter 35')],
                widget=forms.Select,
                label="VA Chapter"
            )
            self.fields['major'] = forms.CharField(label="Major", initial="Displayed from system", disabled=True)
            self.fields['intended_major'] = forms.CharField(label="Intended Major", required=True)
            self.fields['certified_hours'] = forms.IntegerField(
                label="Number of hours to be certified for this term",
                required=True
            )

        # TWO forms merged from JAW MOOSE
        elif form_name == "RCE Exam Evaluation":
            self.fields['student_name'] = forms.CharField(label="Name", required=True)
            self.fields['exam_date'] = forms.DateField(label="Exam Date", widget=forms.DateInput(attrs={'type': 'date'}))
            self.fields['psid'] = forms.CharField(label="PSID", required=True)
            self.fields['semester'] = forms.CharField(label="Semester", required=True)

            self.fields['communication_oral'] = forms.ChoiceField(
                label="Communicate effectively orally",
                choices=[('Below Expectations', 'Below Expectations'),
                        ('Meets Expectations', 'Meets Expectations'),
                        ('Above Expectations', 'Above Expectations')]
            )
            self.fields['communication_writing'] = forms.ChoiceField(
                label="Communicate effectively in writing",
                choices=[('Below Expectations', 'Below Expectations'),
                        ('Meets Expectations', 'Meets Expectations'),
                        ('Above Expectations', 'Above Expectations')]
            )
            self.fields['research_problem'] = forms.ChoiceField(
                label="Defined the research problem",
                choices=[('Below Expectations', 'Below Expectations'),
                        ('Meets Expectations', 'Meets Expectations'),
                        ('Above Expectations', 'Above Expectations')]
            )
            self.fields['research_eval'] = forms.ChoiceField(
                label="Critically evaluated existing research",
                choices=[('Below Expectations', 'Below Expectations'),
                        ('Meets Expectations', 'Meets Expectations'),
                        ('Above Expectations', 'Above Expectations')]
            )
            self.fields['research_method'] = forms.ChoiceField(
                label="Proposed and justified methods",
                choices=[('Below Expectations', 'Below Expectations'),
                        ('Meets Expectations', 'Meets Expectations'),
                        ('Above Expectations', 'Above Expectations')]
            )
            self.fields['research_results'] = forms.ChoiceField(
                label="Described and interpreted the results",
                choices=[('Below Expectations', 'Below Expectations'),
                        ('Meets Expectations', 'Meets Expectations'),
                        ('Above Expectations', 'Above Expectations')]
            )
            self.fields['comments'] = forms.CharField(label="Comments", widget=forms.Textarea, required=False)
            self.fields['result'] = forms.ChoiceField(label="Pass or Fail", choices=[('Pass', 'Pass'), ('Fail', 'Fail')])

        elif form_name == "Special Request Options":
            self.fields['student_name'] = forms.CharField(label="Student Name", required=True)
            self.fields['student_id'] = forms.CharField(label="Student ID Number", required=True)
            self.fields['degree'] = forms.ChoiceField(
                label="Degree",
                choices=[('Master', 'Master'), ('Doctorate', 'Doctorate')],
                widget=forms.RadioSelect
            )
            self.fields['graduation_date'] = forms.DateField(label="Date of Graduation", widget=forms.DateInput(attrs={'type': 'date'}))
            self.fields['chair_signature'] = forms.CharField(label="Chair/Co-Chair Signature (Type Name)", required=True)
            self.fields['chair_date'] = forms.DateField(label="Chair Signature Date", widget=forms.DateInput(attrs={'type': 'date'}))
            self.fields['student_signature'] = forms.CharField(label="Student Signature (Type Name)", required=True)
            self.fields['student_signature_date'] = forms.DateField(label="Student Signature Date", widget=forms.DateInput(attrs={'type': 'date'}))

            self.fields['request_type'] = forms.MultipleChoiceField(
                label="Special Request Options",
                widget=forms.CheckboxSelectMultiple,
                choices=[
                    ('First Embargo Extension', 'First Embargo Extension'),
                    ('Full Record Hold', 'Full Record Hold'),
                    ('Additional Embargo Extension', 'Additional Embargo Extension'),
                    ('Other', 'Other')
                ]
            )
            self.fields['justification'] = forms.CharField(label="Justification", widget=forms.Textarea, required=True)



        print(f"🛠 Final Fields: {self.fields.keys()}")  # ✅ Debugging output



def clean(self):
    from django.core.files.uploadedfile import InMemoryUploadedFile
    cleaned_data = super().clean()
    form_name = self.initial.get('form_name', '')

    
    # ✅ Exclude file uploads from JSON serialization
    json_ready_data = {}
    for key, value in cleaned_data.items():
        if not isinstance(value, InMemoryUploadedFile):  # ✅ Ignore file uploads
            json_ready_data[key] = value

    print("DEBUG: Cleaned Data Before JSON:", json_ready_data)  # ✅ Debugging

    # ✅ Convert cleaned data to JSON and store it
    cleaned_data['data'] = json.dumps(json_ready_data)

    return cleaned_data



