# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class User(AbstractUser):

    def __str__(self):
        return self.username

class SlackUser(TimeStampedModel):

    """
    Store data about slack user
    """

    ACCESS_CHOICES = ((True, _('Yes')),
                      (False, _('No')))

    user = models.ForeignKey(User,
                             verbose_name=_('Related user'),
                             related_name='slack_users', blank=True, null=True)

    team = models.CharField(_('Team'), max_length=255)
    slack_id = models.CharField(_('Slack ID'), max_length=255)
    name = models.CharField(_('username'), blank=True, max_length=255)
    real_name = models.CharField(_('Real name'), blank=True, max_length=255)
    first_name = models.CharField(_('First name'), max_length=255, blank=True)
    last_name = models.CharField(_('Last name'), max_length=255, blank=True)
    email = models.CharField(_('Email'), blank=True, max_length=255)
    commands_access = models.BooleanField(_('Can execute commands'), default=True, choices=ACCESS_CHOICES)
    timezone = models.CharField(_('Timezone'), blank=True, max_length=100)
    is_owner = models.BooleanField(_('Is owner'), blank=True, default=False)
    is_admin = models.BooleanField(_('Is admin'), blank=True, default=False)
    is_deleted = models.BooleanField(_('Is deleted'), default=False)

    def __str__(self):
        return self.name if self.name else '@'.join([self.slack_id, self.team])

    class Meta:
        unique_together = ('team', 'slack_id')
