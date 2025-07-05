from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Lesson, Course


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj).count()



