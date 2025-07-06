import pytest
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from apps.community import models

User = get_user_model()

@pytest.mark.django_db
def test_create_community():
    user = User.objects.create_user(email='owner@company.com', password='pass')
    community = models.Community.objects.create(
        name='Test Community',
        slug='test-community',
        description='A test community',
        owner=user
    )
    assert community.name == 'Test Community'
    assert community.owner == user
    assert community.slug == 'test-community'

@pytest.mark.django_db
def test_group_belongs_to_community():
    user = User.objects.create_user(email='owner@company.com', password='pass')
    community = models.Community.objects.create(
        name='Test Community',
        slug='test-community',
        owner=user
    )
    group = models.Group.objects.create(
        name='Test Group',
        community=community,
        position=1
    )
    assert group.community == community
    assert group.position == 1

@pytest.mark.django_db
def test_space_creation_and_moderators():
    user = User.objects.create_user(email='owner@company.com', password='pass')
    mod = User.objects.create_user(email='mod@company.com', password='pass')
    community = models.Community.objects.create(
        name='Test Community',
        slug='test-community',
        owner=user
    )
    group = models.Group.objects.create(
        name='Test Group',
        community=community
    )
    space = models.Space.objects.create(
        name='Test Space',
        slug='test-space',
        group=group,
        community=community,
        visibility='private'
    )
    space.moderators.add(mod)
    assert space.moderators.count() == 1
    assert mod in space.moderators.all()
    assert space.visibility == 'private'

@pytest.mark.django_db
def test_membership_unique_constraint():
    user = User.objects.create_user(email='member@company.com', password='pass')
    owner = User.objects.create_user(email='owner@company.com', password='pass')
    community = models.Community.objects.create(
        name='Test Community',
        slug='test-community',
        owner=owner
    )
    group = models.Group.objects.create(
        name='Test Group',
        community=community
    )
    space = models.Space.objects.create(
        name='Test Space',
        slug='test-space',
        group=group,
        community=community
    )
    membership1 = models.Membership.objects.create(user=user, space=space)
    with pytest.raises(Exception):
        models.Membership.objects.create(user=user, space=space)

@pytest.mark.django_db
def test_post_and_comment_creation():
    user = User.objects.create_user(email='poster@company.com', password='pass')
    owner = User.objects.create_user(email='owner@company.com', password='pass')
    community = models.Community.objects.create(
        name='Test Community',
        slug='test-community',
        owner=owner
    )
    group = models.Group.objects.create(
        name='Test Group',
        community=community
    )
    space = models.Space.objects.create(
        name='Test Space',
        slug='test-space',
        group=group,
        community=community
    )
    post = models.Post.objects.create(
        user=user,
        space=space,
        title='Test Post',
        content='Post content'
    )
    comment = models.Comment.objects.create(
        post=post,
        user=user,
        content='A comment'
    )
    assert post.title == 'Test Post'
    assert comment.post == post
    assert comment.user == user

@pytest.mark.django_db
def test_comment_threading():
    user = User.objects.create_user(email='poster@company.com', password='pass')
    owner = User.objects.create_user(email='owner@company.com', password='pass')
    community = models.Community.objects.create(
        name='Test Community',
        slug='test-community',
        owner=owner
    )
    group = models.Group.objects.create(
        name='Test Group',
        community=community
    )
    space = models.Space.objects.create(
        name='Test Space',
        slug='test-space',
        group=group,
        community=community
    )
    post = models.Post.objects.create(
        user=user,
        space=space,
        title='Test Post',
        content='Post content'
    )
    parent_comment = models.Comment.objects.create(
        post=post,
        user=user,
        content='Parent comment'
    )
    child_comment = models.Comment.objects.create(
        post=post,
        user=user,
        content='Child comment',
        parent=parent_comment
    )
    assert child_comment.parent == parent_comment
    assert models.Comment.objects.filter(
        parent__id=parent_comment.id
    ).count() == 1