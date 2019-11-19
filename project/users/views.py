from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from requests import Request

from users.serializers import UserSerializer, UniversitySerializer
from users.models import MainUser, Activation, University
from users.permissions import UniPermission

import constants


class UserViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = MainUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post']

    @action(detail=False, methods=['post'])
    def register(self, request, pk=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            activation = Activation.objects.create(user=user)
            params = {
                'id': user.activation.id,
            }
            r = Request('GET',
                        f'{request.build_absolute_uri("/")}users/activate/',
                        params=params) \
                .prepare()
            send_mail(
                subject='Account verification',
                message = 'To activate your account click link below\n' + r.url,
                from_email = constants.GMAIL_EMAIL,
                recipient_list = [serializer.data.get('email'), ],
                fail_silently = False,
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def activate(self, request, pk=None):
        id = request.GET.get('id')
        try:
            activation = Activation.objects.get(id=id)
        except Activation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not activation.is_active:
            return Response({"Success": 'User is already activated'}, status.HTTP_200_OK)
        if activation.user:
            activation.is_active = False
            user = activation.user
            user.is_active = True
            activation.save()
            user.save()
            return Response({"Success": "Your account is now activeted!"}, status=status.HTTP_200_OK)
        return Response({"Error": 'User not found'}, status.HTTP_404_NOT_FOUND)

class UniViewset(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = (UniPermission,)