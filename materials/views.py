from django.shortcuts import get_object_or_404, render
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from .paginators import StandardResultsSetPagination
from materials.models import Course, Lesson, Subscription
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwnerOrModer

from .stripe_service import (
    create_stripe_product,
    create_stripe_price,
    create_checkout_session,
)
from users.models import Payment


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModer]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name="Модераторы").exists():
            return qs.filter(owner=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name="Модераторы").exists():
            raise PermissionDenied()
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name="Модераторы").exists():
            return qs.filter(owner=self.request.user)
        return qs


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name="Модераторы").exists():
            return qs.filter(owner=self.request.user)
        return qs


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModer]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModer]


class SubscriptionToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course")
        course = get_object_or_404(Course, pk=course_id)
        sub_qs = Subscription.objects.filter(user=request.user, course=course)

        if sub_qs.exists():
            sub_qs.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=request.user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})


class CheckoutSessionAPIView(APIView):
    """
    Создаёт в Stripe Product→Price→Checkout Session,
    сохраняет данные в модели Payment и возвращает клиенту URL оплаты.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1) Получаем ID курса из запроса
        course_id = request.data.get("course")
        course = get_object_or_404(Course, pk=course_id)

        # 2) Stripe: product, price, session
        prod_id = create_stripe_product(course)
        price_id = create_stripe_price(course, prod_id)
        session_id, checkout_url = create_checkout_session(
            course, price_id, request.user
        )

        # 3) Сохраняем запись о платеже
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            payment_method="stripe",
            stripe_product_id=prod_id,
            stripe_price_id=price_id,
            stripe_session_id=session_id,
            checkout_url=checkout_url,
        )

        # 4) Отдаём клиенту ссылку на оплату
        return Response({"checkout_url": checkout_url})
