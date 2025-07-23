from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Владелец",
        null=True,
        blank=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Введите описание курса",
        verbose_name="Описание курса",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена курса", default=0
    )
    photo = models.ImageField(
        upload_to="materials/photo",
        verbose_name="Фото",
        blank=True,
        null=True,
        help_text="Загрузите превью курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Урок", help_text="Укажите урок"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="Выберите курс",
        blank=True,
        null=True,
        related_name="lessons",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Владелец",
        null=True,
        blank=True,
    )
    photo = models.ImageField(
        upload_to="materials/photo",
        verbose_name="Фото",
        blank=True,
        null=True,
        help_text="Загрузите превью урока",
    )
    video_link = models.TextField(
        verbose_name="Ссылка на видео",
        help_text="Введите ссылку на видео",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание урока",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Payment(models.Model):
    stripe_product_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Stripe Product ID"
    )
    stripe_price_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Stripe Price ID"
    )
    stripe_session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Stripe Session ID"
    )
    checkout_url = models.URLField(blank=True, null=True, verbose_name="Checkout URL")


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscribers",
        verbose_name="Курс",
    )

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.email} → {self.course.name}"
