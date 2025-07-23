from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .validators import validate_youtube_link
from materials.models import Course, Lesson
from rest_framework import serializers
from .models import Subscription


class LessonSerializer(ModelSerializer):
    video_link = serializers.CharField(
        allow_blank=True, required=False, validators=[validate_youtube_link]
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.subscribers.filter(user=user).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("user", "course")
        read_only_fields = ("user",)
