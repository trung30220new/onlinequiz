from django.db import models

from student.models import Student
class Course(models.Model):
    course_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    def __str__(self):
        return self.course_name

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)
    # is_true_false = models.BooleanField(default=False)  # New True/False field
    def __str__(self):
        return "ques: " + str(self.id)

class Exam(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    ques=models.JSONField()
    exam_code=models.CharField(max_length=200)
    start=models.DateTimeField(null=True)
    duration_minutes=models.PositiveIntegerField()
    number_of_ques=models.PositiveIntegerField(default=10)
    def __str__(self):
        return 'exam: ' + str(self.id) + ' ' + str(self.start)

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    # exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return 'result: ' + str(self.marks) + ' ' + str(self.date)
