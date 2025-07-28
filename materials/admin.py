from django.contrib import admin

from .models import Course, Lesson
from .models import Subscription

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Subscription)
