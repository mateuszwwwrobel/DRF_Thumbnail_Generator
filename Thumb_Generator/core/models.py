from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image as PilImage
from django.core.files import File
from io import BytesIO


class Plan(models.Model):
    name = models.CharField(max_length=20, unique=True)
    image_height = models.PositiveIntegerField()
    uploaded_file_url = models.BooleanField(default=False)
    expiring_url = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} Plan"


class CustomUser(AbstractUser):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        basic_plan = Plan.objects.get_or_create(name='Basic', image_height=200)[0]
        premium_plan = Plan.objects.get_or_create(
            name='Premium',
            image_height=400,
            uploaded_file_url=True)[0]
        enterprise_plan = Plan.objects.get_or_create(
            name='Enterprise',
            image_height=400,
            uploaded_file_url=True,
            expiring_url=True)[0]
        self.plan = basic_plan
        super().save(*args, **kwargs)


class Image(models.Model):
    original_size_image = models.ImageField(upload_to='images')
    image_200px = models.ImageField(upload_to='images_200px', blank=True, null=True)
    image_400px = models.ImageField(upload_to='images_400px', blank=True, null=True)
    image_custom_size = models.ImageField(upload_to='images_custom_size', blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_size_image}"

    class Meta:
        ordering = ('-added_on',)

    @staticmethod
    def resize_image(image: File, base_height: int) -> File:
        """Makes image of given height from given image"""

        extension = image.file.content_type.split('/')[1]
        im = PilImage.open(image)
        im.convert('RGB')
        h_percent = (base_height / float(im.size[1]))
        w_size = int((float(im.size[0]) * float(h_percent)))
        im = im.resize((w_size, base_height), PilImage.ANTIALIAS)
        thumb_io = BytesIO()
        im.save(thumb_io, extension, quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

    def save(self, *args, **kwargs) -> None:
        self.image_200px = self.resize_image(self.original_size_image, 200)
        self.image_400px = self.resize_image(self.original_size_image, 400)

        # If custom plan exists:
        if self.user.plan.name not in ['basic', 'premium', 'enterprise']:
            self.image_custom_size = self.resize_image(self.original_size_image, self.user.plan.image_height)

        super().save(*args, **kwargs)
