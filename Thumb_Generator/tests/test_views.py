from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from django.urls import reverse
from rest_framework import status

from core.models import CustomUser, Image


class ImageCreateViewTest(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(username='testuser')
        self.user.set_password('testpassword')
        self.user.save()
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        self.list_url = reverse('image-create')

    def test_check_if_user_logged_in(self) -> None:
        logged_in = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(logged_in)

    def test_create(self):
        """POST to create an Image."""
        test_image = self.mock_small_image()
        data = {
            'original_size_image': test_image,
        }

        self.assertEqual(Image.objects.count(), 0)
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)

    @staticmethod
    def mock_small_image() -> File:
        small_image = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        image = SimpleUploadedFile('small.png', small_image, content_type='image/png')
        return image


class ImageListViewTest(TestCase):

    def setUp(self) -> None:
        user = CustomUser.objects.create(username='testuser')
        user.set_password('testpassword')
        user.save()
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        self.list_url = reverse('image-list')

    def test_check_if_user_logged_in(self) -> None:
        logged_in = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(logged_in)

    def test_get_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
