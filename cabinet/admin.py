from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'get_groups', 'lesson', 'type')
    prepopulated_fields = {'slug': ('teacher', 'lesson', 'groups', 'type')}


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('time', 'classroom', 'lesson')
    prepopulated_fields = {'slug': ('classroom', 'lesson')}


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('mark', 'student', 'timetable')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


#admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(Review)
# admin.site.register(Lesson)
#admin.site.register(Mark)
#admin.site.register(Timetable)