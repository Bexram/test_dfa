from django.contrib.auth.models import User
from rest_framework import serializers

from gallery.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('__all__')


class CreatePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ('user',)

    def create(self, validated_data):
        user_data = validated_data
        user_data['user'] = self.context['request'].user
        return Photo.objects.create(**user_data)


class UserSerializer(serializers.ModelSerializer):
    photo = PhotoSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'photo')


class RegistrateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)
