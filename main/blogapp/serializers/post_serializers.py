from django.contrib.auth import get_user_model
from main.blogapp.models import Post
from rest_framework import serializers
User = get_user_model()


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


