from django.shortcuts import render, redirect, reverse
from django.utils.timezone import now

from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from teacher import models as TMODEL


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'student/studentclick.html')


def student_signup_view(request):
    userForm = forms.StudentUserForm()
    studentForm = forms.StudentForm()
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = forms.StudentUserForm(request.POST)
        studentForm = forms.StudentForm(request.POST, request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request, 'student/studentsignup.html', context=mydict)


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    courses = QMODEL.Course.objects.all()
    exams = QMODEL.Exam.objects.all()
    return render(request, 'student/student_dashboard.html',
                  {'courses': courses, 'exams': exams})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_marks.html', {'courses': courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request, exam_id):
    exam = QMODEL.Exam.objects.get(id=exam_id)
    course = exam.course
    total_questions = QMODEL.Question.objects.all().filter(
        course=course).count()
    questions = QMODEL.Question.objects.all().filter(course=course)
    total_marks = 0
    for q in questions:
        total_marks = total_marks + q.marks

    return render(
        request, 'student/take_exam.html', {
            'course': course,
            'exam': exam,
            'total_questions': total_questions,
            'total_marks': total_marks
        })


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request, exam_id):
    print(f'exam id: {exam_id}')
    exam = QMODEL.Exam.objects.get(id=exam_id)
    course = exam.course
    questions = QMODEL.Question.objects.all().filter(course=course)

    # Calculate the expiration time
    exam_end_time = exam.start + timedelta(minutes=exam.duration_minutes)

    # Check if the current time is before the exam's start time
    if exam.start is not None:
        if now() < exam.start:
            print(now())
            print(exam.start)
            print(request, "The exam has not started yet. Please check back later.")
            return render(request, 'student/exam_not_started.html', {
                'exam': exam,
                'course': course,
            })
        elif now() > exam_end_time:
            return render(request, 'student/exam_expired.html', {
                'exam': exam,
                'course': course,
            })

    delta = now() - exam.start
    # Calculate delta in minutes
    minutes = round(delta.total_seconds() / 60, 2)
    print(f"Delta in minutes: {minutes}")

    if request.method == 'POST':
        pass
    response = render(request, 'student/start_exam.html', {
        'course': course,
        'exam': exam,
        'questions': questions,
        'minutes': minutes
    })
    response.set_cookie('course_id', course.id)
    response.set_cookie('exam_id', exam.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('exam_id') is not None:
        exam_id = request.COOKIES.get('exam_id')
        exam = QMODEL.Exam.objects.get(id=exam_id)

        # Calculate the expiration time
        exam_end_time = exam.start + timedelta(minutes=exam.duration_minutes)

        if now() > exam_end_time:
            return render(request, 'student/exam_expired.html', {
                'exam': exam,
            })

        course = exam.course

        total_marks = 0
        questions = QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):

            selected_ans = request.COOKIES.get(str(i + 1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks = total_marks
        result.exam = exam
        result.student = student
        result.save()

        return HttpResponseRedirect('view-result')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses = QMODEL.Course.objects.all()
    exams = QMODEL.Exam.objects.all()
    print(f'size {len(exams)}')
    return render(request, 'student/view_result.html',
                  {'courses': courses, 'exams': exams})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request, exam_id):
    print(f'view {exam_id}')
    exam = QMODEL.Exam.objects.get(id=exam_id)
    pk = exam.course.id
    course = QMODEL.Course.objects.get(id=pk)
    print(f'view {course}')
    student = models.Student.objects.get(user_id=request.user.id)
    results = QMODEL.Result.objects.all().filter(exam=exam).filter(
        student=student)
    return render(request, 'student/check_marks.html', {'results': results})
