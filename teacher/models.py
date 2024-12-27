from django.db import models
from django.contrib.auth.models import User

from quiz.models import Course


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/Teacher/',
                                    null=True,
                                    blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    status = models.BooleanField(default=False)
    salary = models.PositiveIntegerField(null=True)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        # return self.user.first_name
        return f"pk: {self.user.pk}, uid: {self.user.id}, id: {self.id}, username: {self.user.username}"


class TeacherCourse(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"teacher: {self.teacher.user.username}, course: {self.course.course_name}"
