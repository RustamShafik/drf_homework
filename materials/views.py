from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsModer
from rest_framework.exceptions import PermissionDenied

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from django.shortcuts import render


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated | IsModer]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated & IsModer]
        elif self.action == "create":
            permission_classes = [IsAuthenticated & ~IsModer]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated & ~IsModer]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name="Модераторы").exists():
            raise PermissionDenied()
        serializer.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if not self.request.user.groups.filter(name="Модераторы").exists():
            raise PermissionDenied()
        serializer.save()


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_destroy(self, instance):
        if self.request.user.groups.filter(name="Модераторы").exists():
            raise PermissionDenied()
        instance.delete()
