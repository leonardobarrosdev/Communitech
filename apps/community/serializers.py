from rest_framework import serializers
from apps.community.models import Community, Space, Post, Comment, Group


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = "__all__"
        read_only_fields = ["created_at"]
        extra_kwargs = {"slug": {"required": False}}


class CommunityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = "__all__"
        read_only_fields = ["created_at"]
        extra_kwargs = {"slug": {"required": False}, "owner": {"required": False}}


class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = "__all__"
        read_only_fields = ["created_at"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["created_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["created_at"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
