from django import forms
import json
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['form_name', 'signature']  # ✅ Remove 'data' from fields (we'll handle it separately)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get logged-in user
        super().__init__(*args, **kwargs)

        form_name = self.initial.get('form_name', '')

        if form_name == "Term Withdrawal Request":
            self.fields['student_name'] = forms.CharField(label="Student Name", required=True)
            self.fields['myuh_id'] = forms.CharField(label="myUH ID", required=True)
            self.fields['last_name'] = forms.CharField(label="Last Name", required=True)
            self.fields['first_name'] = forms.CharField(label="First Name", required=True)
            self.fields['middle_name'] = forms.CharField(label="Middle Name", required=False)
            self.fields['phone'] = forms.CharField(label="Phone #", required=True)
            self.fields['email'] = forms.EmailField(label="Email", initial=user.email if user else '', disabled=True)
            self.fields['program_plan'] = forms.CharField(label="Program/Plan", required=True)
            self.fields['academic_career'] = forms.CharField(label="Academic Career", required=True)

            # Add withdrawal term selection
            self.fields['withdrawal_term'] = forms.ChoiceField(
                choices=[('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer')],
                widget=forms.RadioSelect,
                label="Withdrawal Term"
            )

    def clean(self):
        cleaned_data = super().clean()

        # Automatically convert form inputs into a JSON field
        self.cleaned_data['data'] = json.dumps({
            'student_name': cleaned_data.get('student_name'),
            'myuh_id': cleaned_data.get('myuh_id'),
            'last_name': cleaned_data.get('last_name'),
            'first_name': cleaned_data.get('first_name'),
            'middle_name': cleaned_data.get('middle_name'),
            'phone': cleaned_data.get('phone'),
            'email': cleaned_data.get('email'),
            'program_plan': cleaned_data.get('program_plan'),
            'academic_career': cleaned_data.get('academic_career'),
            'withdrawal_term': cleaned_data.get('withdrawal_term'),
        })

        return cleaned_data
