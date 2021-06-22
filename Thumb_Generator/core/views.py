from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status, generics
from rest_framework.response import Response
from core.models import Image, Plan

from core import serializers


class ImageCreateView(LoginRequiredMixin, generics.CreateAPIView):
    serializer_class = serializers.ImageCreateSerializer

    def create(self, request, *args, **kwargs):
        self.validate_mime_type(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def validate_mime_type(request):
        """Validate image content type. Raise ValueError when image is not PNG or JPG format"""

        image = request.data['original_size_image']
        file_extension = image.content_type.split('/')[1]
        if file_extension not in ['png', 'jpeg']:
            raise ValueError('Wrong file extension. Must be either png or jpeg.')

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ImageListView(LoginRequiredMixin, generics.ListAPIView):

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.user.plan == Plan.objects.get(name='Basic'):
            return serializers.BasicPlanSerializer
        elif self.request.user.plan == Plan.objects.get(name='Premium'):
            return serializers.PremiumPlanSerializer
        elif self.request.user.plan == Plan.objects.get(name='Enterprise'):
            return serializers.EnterprisePlanSerializer
        else:
            return serializers.CustomPlanSerializer
