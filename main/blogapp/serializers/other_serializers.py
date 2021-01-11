from django.contrib.auth import get_user_model
from rest_flex_fields import FlexFieldsModelSerializer
from main.blogapp.models import Image
from versatileimagefield.serializers import VersatileImageFieldSerializer
User = get_user_model()


class ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
        ]
    )

    class Meta:
        model = Image
        fields = ['pk', 'name', 'image']
