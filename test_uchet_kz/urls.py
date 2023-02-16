from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from todolist.views import LogoutAPIView, MyTokenObtainPairView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutAPIView.as_view(), name="logout"),

    path("api/", include('todolist.urls')),

]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()