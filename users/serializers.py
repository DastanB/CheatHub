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


class ProfileShortSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    avatar_full_path = serializers.SerializerMethodField()
    university_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('user_name', 'bio', 'avatar_full_path', 'university_name')

    def get_user_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def get_avatar_full_path(self, obj):
        if obj.avatar:
            return self.context['request'].build_absolute_uri(obj.avatar.url)
        return ''

    def get_university_name(self, obj):
        if obj.university:
            return obj.university.name
        return ''


class ProfileFullReadSerializer(serializers.ModelSerializer):
    user = UserFullSerializer(read_only=True)
    university = UniversityFullSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileFullWriteSerializer(serializers.ModelSerializer):
    user = UserFullSerializer(read_only=True)
    university = UniversityFullSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'