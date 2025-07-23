from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import SubscriptionToggleAPIView
from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonCreateApiView,
    LessonDestroyApiView,
    LessonListApiView,
    LessonRetrieveApiView,
    LessonUpdateApiView,
)
from .views import CheckoutSessionAPIView

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyApiView.as_view(),
        name="lessons_delete",
    ),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"
    ),
    path(
        "courses/subscribe/",
        SubscriptionToggleAPIView.as_view(),
        name="course_subscribe",
    ),
    path(
        "payments/checkout/", CheckoutSessionAPIView.as_view(), name="payments_checkout"
    ),
]

urlpatterns += router.urls
