# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from slackclient import SlackClient


class SlackApiHelper(object):

    API_URL = 'https://slack.com/api/'

    def __init__(self, token, team_id, *args, **kwargs):
        """
        token - token for authenticated user
        team_id - id of authenticated team
        """
        assert isinstance(token, str)
        assert isinstance(team_id, str)
        self.token = token
        self.team_id = team_id
        self.client = SlackClient(token)

    def get_team_members_list(self):
        response = self.client.api_call('users.list')
        if not response or 'ok' not in response:
            return []
        return response.get('members')

    def send_slackbot_message(self, channel, message):
        """
        Send message as slack bot
        """
        assert isinstance(channel, str)
        assert isinstance(message, str) or isinstance(message, dict)
        return self.client.api_call('chat.postMessage', channel=channel, text=message, as_user=False)
