from django.contrib.auth import get_user_model
from main.blogapp.models import Post, Comment
from rest_framework import serializers
User = get_user_model()


class CommentInputSerializer(serializers.Serializer):
    comment_text = serializers.CharField(max_length=300)
    post = serializers.IntegerField()
    pk = serializers.SerializerMethodField()

    def create(self, validated_data):
        post_pk = validated_data.pop('post') # in this way you can add any field to the serializer, for your need, if it does not
        # conform to your model, then pop it before creating Model objects with the command Comment.objects.create
        post_from_db = Post.objects.get(pk=post_pk)
        comment = Comment.objects.create(**validated_data)
        comment.post = post_from_db
        comment.save()
        username = self.context["username"]
        user_fetched = User.objects.filter(username=username).first()
        if user_fetched:
            comment.author = user_fetched

        comment.save()
        return comment

    def get_pk(self,obj):
        return obj.id


class CommentOutputSerializer(serializers.ModelSerializer):
    pk = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['comment_text','pk']

    def get_pk(self,obj):
        return obj.id


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('comment_text','pk')
