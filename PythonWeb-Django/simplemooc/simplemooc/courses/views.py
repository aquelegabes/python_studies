from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement
from .forms import ContactCourse, CommentForm

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
def announcements(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment,
            user=request.user, course=course
        )
        if not enrollment.is_approved():
            messages.error(request, 'A sua inscrição está pendente')
            return redirect('accounts:dashboard')

    template = 'courses/announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request, template, context)

@login_required
def show_announcement(request, slug, pk):

    course = get_object_or_404(Course, slug=slug)

    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment,
            user=request.user, course=course
        )
        if not enrollment.is_approved():
            messages.error(request, 'A sua inscrição está pendente')
            return redirect('accounts:dashboard')
    
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