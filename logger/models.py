from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.db import models


class Log(models.Model):

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

    #item = models.ForeignKey()

    action_type = models.IntegerField(choices=ActionChoices.choices)

    content = models.JSONField(null=False)