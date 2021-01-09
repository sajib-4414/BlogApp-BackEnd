from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
