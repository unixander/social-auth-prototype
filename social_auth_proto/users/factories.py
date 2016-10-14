# encoding: utf-8
from __future__ import unicode_literals

import factory

from django.contrib.auth.hashers import make_password
from django.utils import lorem_ipsum

from social.apps.django_app.default.models import UserSocialAuth

from social_auth_proto.users.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', )

    @factory.lazy_attribute
    def first_name(self):
        return lorem_ipsum.words(1, False)

    @factory.lazy_attribute
    def last_name(self):
        return lorem_ipsum.words(1, False)

    @factory.lazy_attribute
    def email(self):
        return u'{}@example.com'.format(self.username)

    username = factory.Sequence(lambda n: 'user_{0}'.format(n))
    password = make_password('qwerty12')


class UserSocialAuthFactory(factory.DjangoModelFactory):

    class Meta:
        model = UserSocialAuth

    @factory.lazy_attribute
    def provider(self):
        return 'slack'

    @factory.lazy_attribute
    def uid(self):
        return lorem_ipsum.words(2, False)

    @factory.lazy_attribute
    def extra_data(self):
        return {
            'id': lorem_ipsum.words(1, False),
            'team_id': lorem_ipsum.words(1, False),
            'access_token': lorem_ipsum.words(1, False),
            'bot': {
                'bot_user_id': 'test_id',
                'bot_access_token': 'access_token'
            }
        }
