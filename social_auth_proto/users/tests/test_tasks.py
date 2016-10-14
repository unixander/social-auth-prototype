# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mock

from django.test import TestCase

from social_auth_proto.users.tests.api_utils import SlackAPIMock
from social_auth_proto.users.factories import UserFactory, UserSocialAuthFactory
from social_auth_proto.users.models import SlackUser
from social_auth_proto.users.tasks import update_team_members_list

class TestUpdateTeamMembersList(TestCase):

    def setUp(self):
        self.user = UserFactory.create()
        extra_data = {
            'id': 'U18K6UZDK',
            'team_id': 'T18KBHTA5',
            'access_token': 'test_access_token'
        }
        self.social_auth = UserSocialAuthFactory.create(user=self.user, extra_data=extra_data)

    @mock.patch('slackclient.SlackClient.api_call', side_effect=SlackAPIMock.handle_post)
    def test_initial_update_team_members_list(self, mock_call):
        """
        Test initial slack list fill
        """
        update_team_members_list(self.user)

        self.assertEqual(SlackUser.objects.count(), 3)
        self.assertEqual(SlackUser.objects.filter(user_id=self.user.id).count(), 1)
        self.assertTrue(SlackUser.objects.filter(team='T18KBHTA5', slack_id='U2A1DAC7R').exists())
        self.assertTrue(SlackUser.objects.filter(team='T18KBHTA5', slack_id='U18K6UZDK').exists())
        self.assertTrue(SlackUser.objects.filter(team='T18KBHTA5', slack_id='U2A1EB4G5').exists())

    @mock.patch('slackclient.SlackClient.api_call', side_effect=SlackAPIMock.handle_post)
    def test_assign_member_update_team_members_list(self, mock_call):
        """
        Test assigning user to slack member after initial slack list is filled
        """
        update_team_members_list(self.user)

        self.assertEqual(SlackUser.objects.count(), 3)
        self.assertEqual(SlackUser.objects.filter(user_id=self.user.id).count(), 1)
        self.assertTrue(SlackUser.objects.filter(team='T18KBHTA5', slack_id='U2A1DAC7R').exists())
        self.assertTrue(SlackUser.objects.filter(team='T18KBHTA5', slack_id='U2A1DAC7R', user_id__isnull=True).exists())

        extra_data = {
            'id': 'U2A1DAC7R',
            'team_id': 'T18KBHTA5',
            'access_token': 'test_access_token2'
        }
        user = UserFactory.create()
        UserSocialAuthFactory.create(user=user, extra_data=extra_data)

        update_team_members_list(user)
        self.assertEqual(SlackUser.objects.count(), 3)
        self.assertTrue(SlackUser.objects.filter(team='T18KBHTA5', slack_id='U2A1DAC7R', user_id=user.id).exists())
