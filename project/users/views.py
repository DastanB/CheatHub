from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from requests import Request

from users.serializers import UserFullSerializer, ProfileFullSerializer, UniversityFullSerializer
from users.models import MainUser, Activation, Profile, University

import constants


class UserViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = MainUser.objects.all()
    serializer_class = UserFullSerializer
    http_method_names = ['get', 'post']

    def get_permissions(self):
        pass

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


class ProfileViewSet(mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileFullSerializer
    http_method_names = ['put', 'patch']
    parser_classes = (FormParser, MultiPartParser, JSONParser)
    permission_classes = (IsAuthenticated, )

    @action(detail=False, methods=['put', 'patch'])
    def edit_profile(self, request, pk=None):
        profile = request.user.profile
        if request.POST.get('bio'):
            profile.bio = request.POST.get('bio')
        if request.POST.get('avatar'):
            profile.avatar = request.POST.get('avatar')
        if request.POST.get('university'):
            try:
                university = University.objects.get(request.POST.get('university'))
            except University.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            profile.university = university
        profile.save()


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversityFullSerializer
    permission_classes = (IsAdminUser,)
