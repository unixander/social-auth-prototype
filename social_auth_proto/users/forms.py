# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from social_auth_proto.users.models import SlackUser


class SlackUserForm(forms.ModelForm):

    class Meta:
        model = SlackUser
        exclude = ('id',)
