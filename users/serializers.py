from rest_framework import serializers
from users.models import MainUser, Profile, University


class UserFullSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = MainUser.objects.create_user(**validated_data)
        return user

      
class UniversityFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class ProfileFullSerializer(serializers.ModelSerializer):
    user = UserFullSerializer
    university = UniversityFullSerializer

    class Meta:
        model = Profile
        fields = '__all__'
