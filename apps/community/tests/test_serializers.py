import pytest, random
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.community.models import (
    Community, Space, Post, Comment, Group
)
from apps.community.serializers import (
    SpaceSerializer,
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    CommunitySerializer
)

@pytest.fixture
def get_user():
    User = get_user_model()
    generate_name = f"test{random.randint(1, 100)}"
    return User.objects.create_user(
        email=f"{generate_name}@example.com",
        password="StrongPass123!",
        first_name="Test",
        last_name="User"
    )

@pytest.fixture
def get_community(get_user):
    return Community.objects.create(
        name="New Community",
        description="Testing community",
        owner=get_user
    )

@pytest.fixture
def get_space(get_group, get_community):
    return Space.objects.create(
        name="Test Space", group=get_group, community=get_community
    )

@pytest.fixture
def get_post(get_user, get_space):
    return Post.objects.create(
        title="Test Post",
        content="Content",
        user=get_user,
        space=get_space
    )

@pytest.fixture
def get_comment(get_post, get_user):
    return Comment.objects.create(
        post=get_post, user=get_user, content="Nice!"
    )

@pytest.fixture
def get_group(get_community):
    return Group.objects.create(
        name="Test Group", community=get_community
    )

@pytest.mark.django_db
def test_community_serializer_create(get_user):
    data = {
        "name": "New Community",
        "description": "Testing community",
        "owner": get_user.id
    }
    serializer = CommunitySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    community = serializer.save()
    assert community.name == data["name"]
    assert community.slug is not None

@pytest.mark.django_db
def test_space_serializer_fields(get_space):
    serializer = SpaceSerializer(get_space)
    data = serializer.data
    assert "id" in data
    assert "name" in data
    assert "created_at" in data
    assert data["name"] == "Test Space"

@pytest.mark.django_db
def test_post_serializer_fields(get_post):
    post = get_post
    serializer = PostSerializer(post)
    data = serializer.data
    assert data["title"] == "Test Post"
    assert data["content"] == "Content"
    assert data["space"] == post.space.id
    assert "created_at" in data

@pytest.mark.django_db
def test_comment_serializer_fields(get_comment):
    comment = get_comment
    serializer = CommentSerializer(comment)
    data = serializer.data
    assert data["post"] == comment.post.id
    assert data["content"] == "Nice!"
    assert data["parent"] is None
    assert "created_at" in data

@pytest.mark.django_db
def test_group_serializer_fields(get_group):
    serializer = GroupSerializer(get_group)
    data = serializer.data
    assert "id" in data
    assert data["name"] == "Test Group"

@pytest.mark.django_db
def test_space_serializer_read_only_created_at(get_space):
    serializer = SpaceSerializer(get_space)
    assert "created_at" in serializer.fields
    assert serializer.fields["created_at"].read_only

@pytest.mark.django_db
def test_post_serializer_create(get_user, get_space):
    space = get_space
    data = {
        "title": "New Post",
        "content": "Post content",
        "user": get_user.id,
        "space": space.id
    }
    serializer = PostSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    post = serializer.save()
    assert post.title == "New Post"
    assert post.space == space

@pytest.mark.django_db
def test_comment_serializer_create_with_parent(get_comment, get_user):
    parent_comment = get_comment
    data = {
        "post": parent_comment.post.id,
        "user": get_user.id,
        "parent": parent_comment.id,
        "content": "Child comment",
    }
    serializer = CommentSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    comment = serializer.save()
    assert comment.parent == parent_comment