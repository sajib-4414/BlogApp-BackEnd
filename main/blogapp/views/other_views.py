from rest_flex_fields import FlexFieldsModelViewSet
from main.blogapp.models import Image
from main.blogapp.serializers import ImageSerializer


class ImageViewSet(FlexFieldsModelViewSet):
    """
    this is a ViewSet, so it should support CRUD api
    """
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
