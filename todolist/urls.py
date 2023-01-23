from django.urls import path, include
from rest_framework import routers
from todolist.views import (
    # TaskListCreateAPIView,
    # TaskRUDView,
    TaskExecuteAPIView,
    PasswordRequestResetByEmailAPIView,
    PasswordTokenCheckAPIView,
    PasswordSetNewAPIView, TaskViewSet
)

app_name = "todolist"
router = routers.DefaultRouter()
router.register('todo', TaskViewSet, basename='task')
urlpatterns = [
    # todolist logic
    # path('todo/', TaskListCreateAPIView.as_view()),
    # path('todo/<int:id>/', TaskRUDView.as_view()),
    path('', include(router.urls)),
    path('todo/<int:id>/execute/', TaskExecuteAPIView.as_view()),

    # password reset
    path('password-reset-request/', PasswordRequestResetByEmailAPIView.as_view()),
    path('password-reset-check/<uidb64>/<token>/', PasswordTokenCheckAPIView.as_view()),
    path('password-reset-complete/', PasswordSetNewAPIView.as_view())

]
