from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.db import models
from plants.models import Plant


class Log(models.Model):

    CHOICES = {
        1: 'added',
        2: 'changed',
        3: 'deleted',
    }

    class ActionChoices(models.IntegerChoices):
        ADDITION = 1
        CHANGE = 2
        DELETION = 3

    action_time = models.DateTimeField(
        _('action time'),
        default=timezone.now,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_('user'),
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        null=True,
    )

    action_type = models.IntegerField(
        choices=ActionChoices.choices,
    )

    data = models.JSONField(
        null=False,
    )

    def __str__(self):
        return f"{self.user} {self.CHOICES[self.action_type]} for plant {self.plant.uid}: {str(self.data)}"