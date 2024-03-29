from rest_framework import status, viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from todolist.models import Task, User
from todolist.celery_tasks import send_email_reset_password
from todolist.serializers import TaskListSerializer, TaskCRUDSerializer, PasswordSetNewSerializer, LogoutSerializer, \
    CustomTokenObtainPairSerializer


class TaskViewSet(viewsets.GenericViewSet,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskListSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskCRUDSerializer
        else:
            return TaskCRUDSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user).order_by('-id')
        return super().list(self, request, *args, **kwargs)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(done=False, user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg],
            'user': self.request.user.pk
        }
        obj = get_object_or_404(queryset, **filter_kwargs)

        return obj


class TaskExecuteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        task = Task.objects.get(id=id)
        if task.done is True:
            response = 'Already marked as done'
        else:
            task.done = True
            task.save()
            response = 'Task marked as done'
        return Response(response)


# class TaskListCreateAPIView(ListCreateAPIView):
#     queryset = Task.objects.all().order_by('-id')
#     serializer_class = TaskListSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def perform_create(self, serializer):
#         return serializer.save(done=False, user=self.request.user)

# class TaskRUDView(RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskCRUDSerializer
#     permission_classes = (IsAuthenticated,)
#     lookup_field = 'id'

class PasswordRequestResetByEmailAPIView(APIView):

    def post(self, request):
        email = request.data.get('email', '')
        user = User.objects.filter(email=email).first()
        if user:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            domain = f'http://{current_site}/api'
            endpoint_url = f'api/password-reset-check/{uidb64}/{token}'
            full_url = f'{domain}/{endpoint_url}'
            send_email_reset_password.delay(full_url, domain, email)
            return Response(
                {'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'No user with this email address has been found'}, status=status.HTTP_400_BAD_REQUEST
            )


class PasswordTokenCheckAPIView(APIView):

    def get(self, request, uidb64, token):
        user_id = int(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'error': True}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True, 'uidb64': uidb64, 'token': token})


class PasswordSetNewAPIView(APIView):
    serializer_class = PasswordSetNewSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MyTokenObtainPairView(APIView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
