from django.contrib.auth import get_user_model
from rest_flex_fields import FlexFieldsModelSerializer

from main.blogapp.models import Image

User = get_user_model()
from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer


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


class UserInputOutputSerializer(FlexFieldsModelSerializer):
    password = serializers.CharField(write_only=True)
    user_id = serializers.SerializerMethodField('get_user_id')

    def get_user_id(self, obj):
        return obj.id

    class Meta:
        model = User
        fields = ( 'email', 'username', 'password','first_name', 'last_name', 'image_url','user_id')
        required_spec_dict = {
            'required': True,
            'allow_blank': False
        }
        extra_kwargs = {
            'email': required_spec_dict,
            'image_url': { 'required': False, 'allow_blank': True}#,
            # 'first_name': required_spec_dict,
            # 'last_name': required_spec_dict
        }
        expandable_fields = {
            'image': (ImageSerializer, {'many': False}),
        }

    def create(self, validated_data):
        user = super(UserInputOutputSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
