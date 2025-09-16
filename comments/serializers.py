from rest_framework import serializers
from .models import Comment

class AddCommentSerializer(serializers.Serializer):
    message = serializers.CharField()

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = Comment
        fields = ("user","message")