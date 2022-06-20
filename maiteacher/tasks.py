import sys
sys.path.append("..") 
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from cabinet.models import *
@shared_task
def send_mail_task():
    print("Mail sending.......")
    a = Student.objects.all().first()
    t = Timetable.objects.all().first()
    subject = 'welcome to Celery world'
    message = f'Уважаемый {a.name}, просим оставить отзыв на занятие {t.name} по ссылке http://127.0.0.1:8000/cabinet/reviews/{t.slug}/new/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ["timofey.1234@mail.ru", ]
    send_mail( subject, message, email_from, recipient_list )
    return "Mail has been sent........"