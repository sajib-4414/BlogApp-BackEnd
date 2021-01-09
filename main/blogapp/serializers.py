from django.contrib.auth import get_user_model
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.exceptions import ValidationError
from main.blogapp.models import Image
from rest_framework import serializers
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


class UserCreationSerializer(FlexFieldsModelSerializer):
    password = serializers.CharField(write_only=True)
    user_id = serializers.SerializerMethodField('get_user_id')
    image = ImageSerializer(required=False)  # If you write here ImageSerializer then serializer will expect an integer(which)
    # is primary key here in the payload and also output the same, if you write here ImageSerializer() then the payload
    # have to contain dict and also output the image as dict

    def get_user_id(self, obj):
        return obj.id

    class Meta:
        model = User
        """
        image field works as optional, Need to see why it's automatic behavior is optional
        password is required as it is inside the serializer declared field
        firstname, lastname, is not declared in the serializer, perhaps that is why they are optional
        """
        fields = ('email', 'username', 'password','first_name', 'last_name','user_id','image')
        required_spec_dict = {
            'required': True,
            'allow_blank': False
        }
        extra_kwargs = {
            'email': required_spec_dict
        }
        # expandable_fields = {
        #     'image': (ImageSerializer, {'many': False}),
        # }

    def create(self, validated_data):
        user = super(UserCreationSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False) # add password as write only, so it will not show up
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    image = ImageSerializer  # If you write here ImageSerializer then serializer will expect an integer(which)
    # is primary key here in the payload and also output the same, if you write here ImageSerializer() then the payload
    # have to contain dict and also output the image as dict
    # this serializer is used for inputting data for update so, I used ImageSerializer withouyt bracket, so I can
    # input image ID

    class Meta:
        model = User
        fields = ('email','username','first_name', 'last_name','password','image')

    def update(self, instance, validated_data):
        if 'first_name' in validated_data:
            instance.first_name = validated_data.get('first_name', instance.first_name)
        if 'last_name' in validated_data:
            instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'password' in validated_data:
            instance.set_password(validated_data.get('password'))
        if 'image' in validated_data:
            image_id = validated_data.get('image')
            # image = self.get_image(image_id)
            instance.image = image_id
            # instance.set_password = validated_data.get('password', instance.password)
        instance.save()
        return instance

    def get_email(self,obj):
        return obj.email

    def get_username(self,obj):
        return obj.username

    def get_image(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise ValidationError


class UserOutputSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    """
    This serializer is only used to output user profile
    """
    class Meta:
        model = User
        fields = ('email','username','first_name', 'last_name','image')


