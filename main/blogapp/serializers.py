from django.contrib.auth import get_user_model
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.exceptions import ValidationError
from main.blogapp.models import Image, Post
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


class PostOutputSerializer(serializers.ModelSerializer):
    pk = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['title', 'description','pk']

    def get_pk(self,obj):
        return obj.id


class PostInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500)
    pk = serializers.SerializerMethodField()

    def create(self, validated_data):
        postitem = Post.objects.create(**validated_data)
        username = self.context["username"]
        user_fetched = User.objects.filter(username=username).first()
        if user_fetched:
            postitem.author = user_fetched

        postitem.save()
        return postitem

    def get_pk(self,obj):
        return obj.id


class PostUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False,max_length=200)
    description = serializers.CharField(required=False,max_length=500)
    pk = serializers.SerializerMethodField()
    # is_completed = serializers.BooleanField(required=False)
    # due_datetime = serializers.DateTimeField(input_formats=['%d-%m-%Y %H:%M',],required=False)
    # remind_me_datetime = serializers.DateTimeField(input_formats=['%d-%m-%Y %H:%M',],required=False)
    # priority = serializers.ChoiceField(choices=TodoItem.PRIORITIES,required=False)
    # id = serializers.SerializerMethodField()
    """
    A serializer can either implement create or update methods or both, as per django rest docs. 
    """
    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.title = validated_data.get('title', instance.title)
        if 'description' in validated_data:
            instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def validate(self, data):
        """
        This method can be used later to add any validation, the example here is to demonstrate one validation
        Check that the remind me date is before the before due date.
        """
        # print(data['remind_me_datetime'])
        # if 'remind_me_datetime' in data:
        #     if 'due_datetime' in data:
        #         if not (data['due_datetime'] > data['remind_me_datetime']):
        #             raise serializers.ValidationError({"remind_me_date": "Reminder date has to be before due date"})
        #     else:
        #         instance = getattr(self, 'instance', None)
        #         if not (instance.due_datetime > data['remind_me_datetime']):
        #             raise serializers.ValidationError({"remind_me_date": "Reminder date has to be before due date"})
        return data

    def get_pk(self,obj):
        return obj.id
