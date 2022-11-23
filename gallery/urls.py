from django.urls import path

from gallery.views import CreatePhotoAPIView, GetSelfAPIView, \
    CreateUserAPIView, ClearPhotoAPIView, \
    ReadUpdateDeletePhotoAPIView, ListPhotoAPIView

urlpatterns = [
    path('create_photo/', CreatePhotoAPIView.as_view(), name='create_photo'),
    path('photo/', ListPhotoAPIView.as_view(), name='photo'),
    path('photo/<int:pk>/', ReadUpdateDeletePhotoAPIView.as_view(),name='photo_detail'),
    path('getself/', GetSelfAPIView.as_view()),
    path('signup/', CreateUserAPIView.as_view(), name='signup'),
    path('clearbase/', ClearPhotoAPIView.as_view())
]
