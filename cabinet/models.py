from typing_extensions import Required
from weakref import proxy
from django.db import models
from django.forms import URLField

import markdown2
import jwt

# Create your models here.
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


#Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, help_text="Введите ФИО", null=False)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.user) + ' ' + self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Teacher.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.teacher.save()


class Student(models.Model):
    name = models.CharField(max_length=50, help_text="Введите ФИО")
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    # def save(self, **kwargs):
    #     self.slug = slugify(f"{self.name}")
    #     super(Student, self).save()


class Group(models.Model):
    number = models.CharField(max_length=50, help_text="Введите номер группы")

    def __str__(self):
        return self.number


class Lesson(models.Model):
    name = models.CharField(max_length=200, help_text="Введите наименование предмета")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    # def save(self, **kwargs):
    #     self.slug = slugify(f"{self.name}")
    #     super(Lesson, self).save()


class Mark(models.Model):
    mark = models.CharField(max_length=2, default='', help_text="Введите оценку или Н", verbose_name='Оценка')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name='Студент')
    timetable = models.ForeignKey('Timetable', on_delete=models.PROTECT, verbose_name='Занятие')
    comment = models.TextField(max_length=150, null=True, blank=True, verbose_name='Комментарий')

    def __str__(self):
        return str(self.student) + ', ' + str(self.timetable) + ': ' + str(self.mark)

    def get_absolute_url(self):
        return reverse('log', kwargs={'log_slug': self.timetable.lesson.slug})


class Class(models.Model):
    groups = models.ManyToManyField(Group)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    type = models.CharField(max_length=3, help_text='Введите тип занятия')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def get_groups(self):
        return "\n".join([f"{g.number} " for g in self.groups.all()])

    def __str__(self):
        res = f"{str(self.teacher.name)}, {self.get_groups()}, {str(self.lesson)}"
        return res

    def get_absolute_url(self):
        return reverse('log', kwargs={'log_slug': self.slug})


class Timetable(models.Model):
    time = models.DateTimeField(verbose_name='дата и время')
    classroom = models.CharField(max_length=10, help_text='Введите номер аудитории', verbose_name='Аудитория', blank=True)
    url = models.URLField(max_length=300, verbose_name='Ссылка', blank=True)
    lesson = models.ForeignKey(Class, on_delete=models.CASCADE, unique=False, verbose_name='Занятие')
    name = models.TextField(max_length=300, null=True, blank=True, default='Без темы', verbose_name='Тема занятия')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return f"{self.time.strftime('%d/%m/%y %H:%M')}, {str(self.classroom)}, {str(self.lesson)}"

    def get_absolute_url(self):
        return reverse('timetable')

    def save(self, **kwargs):
        slug = f"{self.classroom}-{self.lesson}-{self.time.strftime('%d-%m-%y-%H-%M')}"
        self.slug = slugify(slug)
        super(Timetable, self).save()


class Review(models.Model):
    lesson = models.ForeignKey(Timetable, on_delete=models.CASCADE, unique=False, verbose_name='Занятие')
    review = models.TextField(max_length=300, null=True, blank=True, verbose_name='Отзыв')

    def __str__(self):
        return f"{self.lesson.slug} - {self.review[:10]}"

    def get_absolute_url(self):
        return reverse('thanks')


class Attendance(models.Model):
    attendance = models.CharField(max_length=2, default='', help_text="н или б или пусто", verbose_name='Посещаемость')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name='Студент')
    timetable = models.ForeignKey('Timetable', on_delete=models.PROTECT, verbose_name='Занятие')

    def __str__(self):
        return str(self.student) + ', ' + str(self.timetable) + ': ' + str(self.attendance)

    def get_absolute_url(self):
        return reverse('log', kwargs={'log_slug': self.timetable.lesson.slug})
