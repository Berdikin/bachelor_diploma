from multiprocessing import AuthenticationError
from tokenize import group
from urllib import request
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class AddTimetableForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__( *args, **kwargs)
        self.fields['classroom'].label = 'Аудитория'
        self.fields['time'].label = 'Дата и время'
        self.fields['lesson'] = TypeTimetableLessonField(queryset=Class.objects.filter(teacher__user=self.request.user), label='Занятие', empty_label='Занятие не выбрано')

    class Meta:
        model = Timetable
        fields = ['time', 'classroom', 'lesson', 'name', 'url']


class AddMarkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.student = Student.objects.filter(slug=kwargs.pop('student_slug'))
        self.timetable = Timetable.objects.filter(slug=kwargs.pop('timetable_slug'))
        super().__init__( *args, **kwargs)
        self.fields['timetable'].queryset = self.timetable
        self.fields['student'].queryset = self.student
        self.fields['student'].initial = self.student[0]
        self.fields['timetable'].initial = self.timetable[0]
        self.fields['timetable'] = TypeMarkTimetableField(queryset=self.timetable, initial=self.timetable[0], label='Дата')

    class Meta:
        model = Mark
        fields = ['student', 'timetable', 'mark', 'comment']


class AddReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.timetable = Timetable.objects.filter(slug=kwargs.pop('slug'))
        super().__init__( *args, **kwargs)
        self.fields['lesson'] = TimetableNameField(queryset=self.timetable, initial=self.timetable[0], label='Занятие')

    class Meta:
        model = Review
        fields = ['lesson', 'review']


class UpdateTimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['time']


class UpdateMarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['mark']

class TypeMarkTimetableField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.time.strftime('%d/%m/%y')

class TypeTimetableLessonField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.lesson}, {obj.get_groups()}"

class TimetableNameField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name}"
