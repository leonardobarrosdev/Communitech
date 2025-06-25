from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class NotificationType(models.Model):
    """
    Tipos de notificação possíveis, definidos pela plataforma.
    Ex.: Curtidas, DMs, Comentários, Nova publicação no espaço X
    """
    CATEGORY_CHOICES = (
        ("activity", _("New activity")),
        ("space_post", _("New publication in space")),
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    space = models.ForeignKey('community.Space', null=True, blank=True, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)  # Apenas leitura, sistema define

    def __str__(self):
        return self.name


class UserNotificationPreference(models.Model):
    """
    Preferências de notificação de um usuário por tipo de notificação
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    via_email = models.BooleanField(default=True)
    via_platform = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'notification_type')
