# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from social.backends.slack import SlackOAuth2

from social_auth_proto.users.tasks import update_team_members_list


class CustomSlackOAuth2(SlackOAuth2):

    EXTRA_DATA = [
        ('id', 'id'),
        ('name', 'name'),
        ('real_name', 'real_name'),
        ('team_id', 'team_id'),
        ('team_name', 'team_name'),
        ('tz', 'tz'),
        ('bot', 'bot'),
        ('is_admin', 'is_admin'),
        ('is_owner', 'is_owner'),
    ]
    name = 'slack'

    def complete(self, *args, **kwargs):
        user = self.auth_complete(*args, **kwargs)
        update_team_members_list.apply_async((user,))
        return user

    def auth_allowed(self, response, details):
        """
        Return True if the user should be allowed to authenticate, by
        default check if email\team is whitelisted (if there's a whitelist)
        """
        emails = self.setting('WHITELISTED_EMAILS', [])
        domains = self.setting('WHITELISTED_DOMAINS', [])
        teams = self.setting('WHITELISTED_TEAM_NAMES', [])
        team = details.get('team_name')
        email = details.get('email')
        allowed = True
        if email and (emails or domains):
            domain = email.split('@', 1)[1]
            allowed = email in emails or domain in domains
        if allowed and team and teams:
            allowed = team in teams
        return allowed

    def get_user_details(self, response):
        """Return user details from Slack account"""
        # Build the username with the team $username@$team_url
        # Necessary to get unique names for all of slack
        username = response.get('user')
        if self.setting('USERNAME_WITH_TEAM', True):
            match = re.search(r'//([^.]+)\.slack\.com', response['url'])
            username = '{0}@{1}'.format(username, match.group(1))

        out = {'username': username}
        if 'profile' in response:
            out.update({
                'email': response['profile'].get('email'),
                'fullname': response['profile'].get('real_name'),
                'first_name': response['profile'].get('first_name'),
                'last_name': response['profile'].get('last_name'),
                'team_name': response.get('team_name')
            })
        return out
