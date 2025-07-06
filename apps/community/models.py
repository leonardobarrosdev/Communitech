from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Community(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug or Community.objects.filter(slug=self.slug).exists():
            base_slug = slugify(self.name)
            unique_slug = base_slug
            num = 1
            while Community.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


class Group(models.Model):
    name = models.CharField(max_length=100)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)


class Space(models.Model):
    VISIBILITY = (
        ('public', 'Público'),
        ('private', 'Privado'),
        ('secret', 'Secreto'),
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=10, choices=VISIBILITY, default='public')
    moderators = models.ManyToManyField(User, related_name='moderated_spaces', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'space')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
