import io

from PIL import Image
from django.urls import reverse
from rest_framework import status
from django.test import TestCase, Client
from .models import *
from .serializers import *

client = Client()


class Login(TestCase):

    def setUp(self):
        test_user = User.objects.create(username='test')
        test_user.set_password('test')
        test_user.save()

    def test_login(self):
        response = client.post(reverse('token_obtain_pair'), data={'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class Signup(TestCase):

    def setUp(self):
        pass

    def test_signup(self):
        response = client.post(reverse('signup'), data={'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PhotoTest(TestCase):

    def setUp(self):
        test_user = User.objects.create(username='test')
        test_user.set_password('test')
        test_user.save()
        Photo.objects.create(
            user=test_user, title='Test1', description='testttt', file='../media/gallery/test.jpg')
        Photo.objects.create(
            user=test_user, title='Test2', description='testttttt1', file='../media/gallery/test.jpg')

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_all_photo(self):
        response = client.get(reverse('photo'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_photo(self):
        response = client.post(reverse('token_obtain_pair'), data={'username': 'test', 'password': 'test'})
        token = response.data['access']
        photo_file = self.generate_photo_file()
        response = client.post(reverse('create_photo'),
                               data={'title': 'test', 'description': 'test', 'file': photo_file},
                               HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_photo(self):
        response = client.post(reverse('token_obtain_pair'), data={'username': 'test', 'password': 'test'})
        token = response.data['access']
        test_photo = Photo.objects.filter(user=User.objects.get(username='test')).first()
        response = client.patch(reverse('photo_detail', kwargs={'pk': test_photo.id}), data={'title': 'test_new'},
                                HTTP_AUTHORIZATION=f'Bearer {token}',
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
