from multiprocessing import AuthenticationError
from django.contrib.auth import logout, login
from django.http import HttpResponse
from .models import *
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.core.mail import send_mass_mail
from .forms import *
from .utils import *


def index(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(-1)
        user_menu.pop(-1)
    context = {
        'title': 'Главная страница',
        'menu': user_menu,
    }
    return render(request, 'cabinet/index.html', context)


class TimetableList(DataMixin, ListView):
    model = Timetable
    template_name = 'cabinet/timetable.html'
    paginate_by = 7 

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Расписание')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Timetable.objects.filter(lesson__teacher__user=self.request.user).order_by('time')
        else:
            return Timetable.objects.all().order_by('time')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'cabinet/login.html'
    extra_context = {'title':'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def logs(request):
    classes = Class.objects.filter(teacher__user=request.user).exclude(type='ЛК')
    lessons = set([cl.lesson for cl in classes])
    groups = {}
    for lesson in lessons:
        classes_lesson = classes.filter(lesson__name=lesson)
        group_list = []
        for class_lesson in classes_lesson:
            for gr in class_lesson.groups.all():
                group_list.append((class_lesson, gr))
        groups[lesson] = group_list
    context = {
        'menu': menu,
        'group_dict': groups,
        'title': "Журналы"
    }
    return render(request, 'cabinet/logs.html', context=context)


@login_required
def log(request, log_slug=None):
    lesson = get_object_or_404(Class, slug=log_slug)
    dates = Timetable.objects.filter(lesson=lesson).order_by('time')#.values('time')
    # dates = [date['time'] for date in dates]
    for group in lesson.groups.all():
        students = Student.objects.filter(group=group).order_by('name')
    marks_q = Mark.objects.filter(timetable__lesson=lesson)
    marks = {}
    for student in students:
        mark_l = marks_q.filter(student=student)
        marks[student] = []
        for date in dates:
            mark = mark_l.filter(timetable=date)#.values('mark')
            if not mark:
                marks[student].append((date, None))
            else:
                marks[student].append((date, mark[0]))
    context = {
        'lesson': lesson,
        'menu': menu,
        'dates': dates,
        'marks': marks,
        'title': f"Журнал группы {lesson.get_groups()}, {lesson.lesson}"
    }
    return render(request, 'cabinet/log.html', context=context)


@login_required
def attendance(request, slug=None):
    lesson = get_object_or_404(Class, slug=slug)
    dates = Timetable.objects.filter(lesson=lesson).order_by('time')#.values('time')
    # dates = [date['time'] for date in dates]
    for group in lesson.groups.all():
        students = Student.objects.filter(group=group).order_by('name')
    attendances_q = Attendance.objects.filter(timetable__lesson=lesson)
    attendances = {}
    for student in students:
        attendance_l = attendances_q.filter(student=student)
        attendances[student] = []
        for date in dates:
            attendance = attendance_l.filter(timetable=date)#.values('attendance')
            if not attendance:
                attendances[student].append((date, None))
            else:
                attendances[student].append((date, attendance[0]))
    context = {
        'lesson': lesson,
        'menu': menu,
        'dates': dates,
        'attendances': attendances,
        'title': f"Журнал группы {lesson.get_groups()}, {lesson.lesson}"
    }
    return render(request, 'cabinet/attendance.html', context=context)


@login_required
def reviews(request):
    classes = Class.objects.filter(teacher__user=request.user)
    lessons = set([cl.lesson for cl in classes])
    res = {}
    for lesson in lessons:
        res[lesson] = {}
        classes_lesson = classes.filter(lesson=lesson)
        for class_lesson in classes_lesson:
            res[lesson][class_lesson.get_groups()] = Timetable.objects.filter(lesson=class_lesson).order_by('time')

    context = {
        'menu': menu,
        'lessons': res,
        'title': "Отзывы"
    }
    return render(request, 'cabinet/reviews.html', context=context)


class ReviewList(LoginRequiredMixin, DataMixin, ListView):
    model = Review
    template_name = 'cabinet/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 7 

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Отзывы')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Review.objects.filter(lesson__slug=self.kwargs['slug'])


def thanks(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(-1)
        user_menu.pop(-1)
    context = {
        'title': 'Спасибо за отзыв!',
        'menu': user_menu,
    }
    return render(request, 'cabinet/thanks.html', context)




class AddTimetable(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddTimetableForm
    template_name = 'cabinet/add_timetable.html'
    login_url = 'login'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление занятия')
        return dict(list(context.items()) + list(c_def.items()))

    def get_form_kwargs(self):
        kwargs = super(AddTimetable, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    

class DeleteTimetable(SuccessMessageMixin, DataMixin, DeleteView):
    model = Timetable
    template_name = 'cabinet/delete_timetable.html'
    success_message = "Занятие из расписания было успешно удалено!"

    def get_success_url(self):
        return reverse_lazy('timetable')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DeleteView, self).delete(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Удаление занятия')
        return dict(list(context.items()) + list(c_def.items()))


class UpdateTimetable(LoginRequiredMixin, DataMixin, UpdateView):
    model = Timetable
    fields = ['time']
    template_name = 'cabinet/update_timetable.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение занятия')
        return dict(list(context.items()) + list(c_def.items()))


class AddMark(LoginRequiredMixin, DataMixin, CreateView):
    model = Mark
    form_class = AddMarkForm
    template_name = 'cabinet/add_mark.html'
    login_url = 'login'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Выставление оценки')
        return dict(list(context.items()) + list(c_def.items()))


    def get_form_kwargs(self):
        kwargs = super(AddMark, self).get_form_kwargs()
        if 'student_slug' in self.kwargs:
            kwargs['timetable_slug'] = self.kwargs['timetable_slug']
            kwargs['student_slug'] = self.kwargs['student_slug']
        return kwargs


class UpdateMark(LoginRequiredMixin, DataMixin, UpdateView):
    model = Mark
    form_class = UpdateMarkForm
    template_name = 'cabinet/update_mark.html'
    login_url = 'login'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение оценки')
        return dict(list(context.items()) + list(c_def.items()))


class DeleteMark(DataMixin, DeleteView):
    model = Mark
    template_name = 'cabinet/delete_mark.html'

    def get_success_url(self):
        return reverse_lazy('logs')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DeleteView, self).delete(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Удаление оценки')
        return dict(list(context.items()) + list(c_def.items()))


class AddReview(DataMixin, CreateView):
    model = Review
    form_class = AddReviewForm
    template_name = 'cabinet/add_review.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Оставьте отзыв')
        return dict(list(context.items()) + list(c_def.items()))

    def get_form_kwargs(self):
        kwargs = super(AddReview, self).get_form_kwargs()
        kwargs['slug'] = self.kwargs['slug']
        return kwargs



def send_mail(request, recipients, lesson, link, subject='Оставьте Ваш отзыв'):
    message = f'Оставьте ваш отзыв на занятие {lesson} по ссылке {link}'
    send_mass_mail((subject, message, settings.EMAIL_HOST_USER, recipients))