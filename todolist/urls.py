from django.urls import path

from todolist.views import TaskListCreateAPIView, TaskRUDView, TaskExecuteAPIView, PasswordRequestResetByEmailAPIView, \
    PasswordTokenCheckAPIView, PasswordSetNewAPIView

app_name = "todolist"
urlpatterns = [
    path('todo/', TaskListCreateAPIView.as_view()),
    path('todo/<int:id>/', TaskRUDView.as_view()),
    path('todo/<int:id>/execute/', TaskExecuteAPIView.as_view()),

    path('password-reset-request/', PasswordRequestResetByEmailAPIView.as_view()),
    path('password-reset-check/<uidb64>/<token>/', PasswordTokenCheckAPIView.as_view()),
    path('password-reset-complete/', PasswordSetNewAPIView.as_view())

]
