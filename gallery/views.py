from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, \
    RetrieveUpdateDestroyAPIView, \
    GenericAPIView, ListAPIView
from rest_framework.response import Response
from .permissions import IsOwner
from gallery.models import Photo
from gallery.serializers import CreatePhotoSerializer,\
    PhotoSerializer, UserSerializer, RegistrateSerializer


class ListPhotoAPIView(ListAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


class CreatePhotoAPIView(CreateAPIView):
    permisson_classes = (permissions.IsAuthenticated,)
    serializer_class = CreatePhotoSerializer


class ReadUpdateDeletePhotoAPIView(RetrieveUpdateDestroyAPIView):
    permisson_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


class GetSelfAPIView(GenericAPIView):
    permisson_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CreateUserAPIView(GenericAPIView):
    serializer_class = RegistrateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            User.objects.get(username=serializer.validated_data['username'])
            return Response('username is busy', status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            new_user = User(username=serializer.validated_data['username'])
            new_user.set_password(serializer.validated_data['password'])
            new_user.save()
            return Response(UserSerializer(new_user).data,
                            status=status.HTTP_201_CREATED)


class ClearPhotoAPIView(GenericAPIView):
    permission_classes = (permissions.IsAdminUser,)

    def delete(self, request):
        Photo.objects.all().delete()
        return Response('аннигиляция успешно завершена',
                        status=status.HTTP_200_OK)
