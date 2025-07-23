from django.shortcuts import render
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
from .paginators import StandardResultsSetPagination
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwnerOrModer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Subscription


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
