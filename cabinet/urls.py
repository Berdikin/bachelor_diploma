from time import time
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('timetable/', TimetableList.as_view(), name='timetable'),
    path('timetable/<slug:slug>/delete/', DeleteTimetable.as_view(), name='delete_timetable'),
    path('timetable/<slug:slug>/update/', UpdateTimetable.as_view(), name='update_timetable'),
    path('add_timetable/', AddTimetable.as_view(), name='add_timetable'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('log/', logs, name='logs'),
    path('log/<slug:log_slug>', log, name='log'),
    path('log/attendance/<slug:slug>', attendance, name='attendance'),
    path('mark/<slug:timetable_slug>/<slug:student_slug>', AddMark.as_view(), name='add_mark'),
    path('mark/<int:pk>/update/', UpdateMark.as_view(), name='update_mark'),
    path('mark/<int:pk>/delete/', DeleteMark.as_view(), name='delete_mark'),
    path('reviews/', reviews, name='reviews'),
    path('reviews/<slug:slug>/', ReviewList.as_view(), name='reviews'),
    path('reviews/<slug:slug>/new/', AddReview.as_view(), name='add_review'),
    path('thanks/', thanks, name='thanks'),
]
