
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from materials.models import Course, Subscription

@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(pk=course_id)
    subs = Subscription.objects.filter(course=course).select_related("user")
    emails = [s.user.email for s in subs if s.user.email]
    if not emails:
        return "No subscribers to notify"

    subject = f"Курс «{course.name}» обновлён"
    message = f"Курс «{course.name}» был обновлён."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, emails)
    return f"Sent to {len(emails)} subscribers"