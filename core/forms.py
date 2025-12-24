from django import forms
from django.core.exceptions import ValidationError
from .models import Student, Teacher, Subject, FeeRecord, Event, School
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        # fields = ['name','email','dob','grade','school']
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email Address'}),
            'dob': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Grade'}),
            'school': forms.Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Hide user field in edit mode
            self.fields.pop('user', None)

    def clean_user(self):
        user = self.cleaned_data.get('user')
        if user:
            if Teacher.objects.filter(user=user).exists():
                raise ValidationError("This User is already associated with a Teacher.")
        return user
        
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        # fields = ['name','email','school','subjects']
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email Address'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Hide user field in edit mode
            self.fields.pop('user', None)

    def clean_user(self):
        user = self.cleaned_data.get('user')
        if user:
            if Student.objects.filter(user=user).exists():
                raise ValidationError("This User is already associated with a Student.")
        return user
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        # fields = ['name','code','school']
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Subject Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Subject Code'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
        }
            
class FeeRecordForm(forms.ModelForm):
    class Meta:
        model = FeeRecord
        # fields = ['student','amount','status',]
        fields = '__all__'  
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Amount'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # fields = ['title','date','description','school']
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Event Title'}),
            'date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Event Description'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
 }
class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        # fields = ['name','address']
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'School Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control','placeholder': 'School Address'}),
        }
        


from django import forms
from .models import Result

from django import forms
from django.core.exceptions import ValidationError
from .models import Result, Subject, Student

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = [
            "school",
            "student",
            "subject",
            "marks_obtained",
            "total_marks",
            "exam_date"
        ]
        widgets = {
            "exam_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initially empty
        self.fields["student"].queryset = Student.objects.none()
        self.fields["subject"].queryset = Subject.objects.none()

        if "school" in self.data:
            try:
                school_id = int(self.data.get("school"))
                school = School.objects.get(id=school_id)

                self.fields["student"].queryset = Student.objects.filter(
                    school=school
                )
                self.fields["subject"].queryset = Subject.objects.filter(
                    school=school
                )

            except (ValueError, School.DoesNotExist):
                pass

        elif self.instance.pk:
            self.fields["student"].queryset = Student.objects.filter(
                school=self.instance.school
            )
            self.fields["subject"].queryset = Subject.objects.filter(
                school=self.instance.school
            )

    # 🔐 BACKEND VALIDATION
    def clean(self):
        cleaned_data = super().clean()
        school = cleaned_data.get("school")
        student = cleaned_data.get("student")
        subject = cleaned_data.get("subject")

        if school and student and student.school != school:
            raise ValidationError("Student does not belong to selected school.")

        if school and subject and subject.school != school:
            raise ValidationError("Subject does not belong to selected school.")

        return cleaned_data