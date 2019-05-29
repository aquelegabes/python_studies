from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement, Lesson
from .forms import ContactCourse, CommentForm
from .decorators import enrollment_required

# Create your views here.
def index(request):
    courses = Course.objects.all()
    template_name = 'courses/index.html'
    context = {
        'courses': courses
    }
    return render(request, template_name, context)

def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            valid = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()
        valid = False

    context = {
        'course': course,
        'form': form,
        'is_valid': valid
    }
    template_name = 'courses/details.html'
    return render(request, template_name, context)

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )

    if created:
        #enrollment.active()
        messages.success(request, 'Você foi inscrito no curso {} com sucesso'.format(course.name))
    else:
        messages.info(request, 'Você já está inscrito no curso {}'.format(course))

    return redirect('accounts:dashboard')

@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course
    )
    if request.POST:
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')
    template = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course,
    }
    return render(request, template, context)

@login_required
@enrollment_required
def announcements(request, slug):
    course = request.course
    template = 'courses/announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request, template, context)

@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course 
    form = CommentForm(request.POST or None)
    announcement = get_object_or_404(course.announcements.all(), pk=pk)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso')

    template = 'courses/show_announcement.html'
    
    context ={
        'course':course,
        'announcement': announcement,
        'form': form
    }

    return render(request, template, context)

@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    lessons = course.released_lessons()

    if request.user.is_staff:
        lessons = course.lessons.all()

    template = 'courses/lessons.html'
    context = {
        'course': course,
        'lessons': lessons
    }
    
    return render(request, template, context)

@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, pk=pk, course=course)

    if not request.user.is_staff and not lesson.is_available():
        messages.error(request,'Esta aula não está disponível')
        return redirect('courses:lessons', slug=course.slug)

    template = 'courses/lesson.html'
    context = {
        'course': course,
        'lesson': lesson
    }
    return render(request, template, context)