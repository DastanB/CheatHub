from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from requests import Request

from users.serializers import UserFullSerializer, ProfileShortSerializer, ProfileFullReadSerializer, \
    ProfileFullWriteSerializer, UniversityFullSerializer
from users.models import MainUser, Activation, Profile, University

import constants
import logging

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.GenericViewSet):
    queryset = MainUser.objects.all()
    http_method_names = ['get', 'post']

    @action(detail=False, methods=['post'])
    def register(self, request, pk=None):
        serializer = UserFullSerializer(data=request.data)
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
            logger.info(f'User with email {serializer.data.get("email")} registered')
            return Response(serializer.data)
        logger.error(f'Registration with email {serializer.data.get("email")} failed \n'
                     f'{serializer.errors}')
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
            logger.info(f'User with email {serializer.data.get("email")} activated')
            return Response({"Success": "Your account is now activeted!"}, status=status.HTTP_200_OK)
        logger.error(f'Activation with email {serializer.data.get("email")} failed \n'
                     f'{serializer.errors}')
        return Response({"Error": 'User not found'}, status.HTTP_404_NOT_FOUND)

      
class ProfileViewSet(viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    http_method_names = ['get', 'put', 'patch']
    parser_classes = (FormParser, MultiPartParser, JSONParser)
    permission_classes = (IsAuthenticated, )

    @action(detail=False, methods=['get'])
    def get_profile(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileShortSerializer(profile,
                                           context={'request': request})
        logger.info(f'Get of profile id: {profile.id}')
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def edit_profile(self, request, pk=None):
        try:
            profile = Profile.objects.get(id=request.user.profile.id)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileFullWriteSerializer(instance=profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'Profile with id: {profile.id} updated')
            return Response(serializer.data)
        logger.error(f'Update of profile id: {profile.id} failed \n'
                     f'{serializer.errors}')
        return Response(serializer.errors)


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversityFullSerializer
    permission_classes = (IsAdminUser,)
