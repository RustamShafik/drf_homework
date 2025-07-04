from rest_framework.routers import SimpleRouter
from materials.views import CourseViewSet, LessonListApiView, LessonCreateApiView, LessonDestroyApiView, LessonUpdateApiView, LessonRetrieveApiView
from materials.apps import MaterialsConfig
from django.urls import path

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lessons_delete"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"),
]

urlpatterns += router.urls