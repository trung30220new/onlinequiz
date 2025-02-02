from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class TeacherSalaryForm(forms.Form):
    salary=forms.IntegerField()

class CourseForm(forms.ModelForm):
    class Meta:
        model=models.Course
        fields=['course_name','question_number','total_marks']

class QuestionForm(forms.ModelForm):

    #this will show dropdown __str__ method course model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in course model and return it
    courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.Question
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

class ExamForm(forms.ModelForm):
    ques = forms.CharField(required=False)  # Override field to make it optional
    start = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M'),
        required=False
    )

    class Meta:
        model=models.Exam
        fields=['exam_code','duration_minutes','number_of_ques','ques','start']

    def clean_start(self):
        start = self.cleaned_data.get('start')
        if start:
            # Ensure the datetime is timezone-aware
            if timezone.is_naive(start):
                # Convert naive datetime to the current time zone
                start = timezone.make_aware(start, timezone.get_current_timezone())
            # Convert to local time (this step may be redundant if already in local time)
            start = timezone.localtime(start)
        return start
