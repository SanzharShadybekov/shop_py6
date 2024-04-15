from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from core.tasks import send_confirm_email_task
from . import serializers
from .send_mail import send_confirm_email

User = get_user_model()


class UserViewSet(ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    # serializer_class = serializers.UserSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.UserSerializer
        elif self.action == 'register':
            return serializers.RegisterSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        return [AllowAny()]

    # api/v1/accounts/register/
    @action(['POST'], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            send_confirm_email_task.delay(user.email, user.activation_code)
        except Exception as e:
            print(e, '!!!!!!!!!')
            return Response({'msg': 'Registered, but troubles with email!',
                             'data': serializer.data}, status=201)
        return Response({'msg': 'Registered and sent mail!',
                         'data': serializer.data}, status=201)

    @action(['GET'], detail=False, url_path='activate/(?P<uuid>[0-9A-Fa-f-]+)')
    def activate(self, request, uuid):
        try:
            user = User.objects.get(activation_code=uuid)
        except User.DoesNotExist:
            return Response({'msg': 'Invalid link or link expired!'}, status=400)

        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response({'msg': 'Successfully activated!'}, status=200)
