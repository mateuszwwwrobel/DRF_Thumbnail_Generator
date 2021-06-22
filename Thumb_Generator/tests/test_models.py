from django.core.files import File
from django.test import TestCase
from core.models import Image, CustomUser, Plan
from django.core.files.uploadedfile import SimpleUploadedFile


class ImageTestCase(TestCase):

    def setUp(self) -> None:
        user = CustomUser.objects.create(username='testuser')
        user.set_password('testtest')
        user.save()
        test_image = self.mock_small_image()

        self.image = Image.objects.create(original_size_image=test_image, user=user)

    def test_str(self) -> None:
        """Test for string representation."""
        self.assertEqual(str(self.image), self.image.original_size_image)

    def test_resize_image(self) -> None:
        mock_img = self.mock_small_image()
        file_image = File(mock_img, name='test.png')
        resize_img = Image.resize_image(file_image, 400)
        self.assertNotEqual(file_image, resize_img)

    @staticmethod
    def mock_small_image() -> SimpleUploadedFile:
        small_image = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        image = SimpleUploadedFile('small.png', small_image, content_type='image/png')
        return image


class PlanTestCase(TestCase):

    def setUp(self) -> None:
        self.plan = Plan.objects.create(name='Basic', image_height=400)

    def test_str(self):
        """Test for string representation."""
        self.assertEqual(str(self.plan), f"{self.plan.name} Plan")

